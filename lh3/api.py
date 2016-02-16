from __future__ import unicode_literals
from builtins import object
import configparser
import hashlib
import os
import requests

# Exists only to distinguish LibraryH3lp errors from other generated
# errors.
class LH3Error(Exception):
    pass

# Represents a connection to the server.
class API(object):
    versions = {
        'v1': '2011-12-03',
        'v2': '2013-07-21',
        'v3': '2016-02-10'
    }

    def __init__(self, config):
        self.salt = config.get('salt')
        self.server = config.get('server')
        self.timezone = config.get('timezone')
        self.version = config.get('version')

        self.username = config.get('username')
        self.password = config.get('password')
        if self.username is None:
            raise LH3Error('provide credentials for server authentication')

        self.session = requests.Session()
        requests.utils.add_dict_to_cookiejar(
            self.session.cookies, {'libraryh3lp-timezone': self.timezone})

        self.login()

    def verify_login(self):
        result = self.session.get(self.api('/auth/verify'))
        return result.ok and result.json().get('success', False)

    def login(self):
        result = self.session.post(
            self.api('/auth/login'),
            data = {'username': self.username, 'password': self.get_password()})
        if not result.ok:
            raise LH3Error('failed to authenticate with server')

        json = result.json()
        if not json.get('success', False):
            raise LH3Error(json.get('error', 'unknown authentication failure'))

        self.account_id = json.get('account_id')

    def get_password(self):
        return self.password or hashlib.sha256(self.salt + self.username).hexdigest()

    def delete(self, version, path = None, **kwargs):
        return self.maybe_json(self.session.delete(self.api(version, path), **kwargs))

    def get(self, version, path = None, **kwargs):
        return self.maybe_json(self.session.get(self.api(version, path), **kwargs))

    def patch(self, version, path = None, **kwargs):
        return self.maybe_json(self.session.patch(self.api(version, path), **kwargs))

    def post(self, version, path = None, **kwargs):
        return self.maybe_json(self.session.post(self.api(version, path), **kwargs))

    def put(self, version, path = None, **kwargs):
        return self.maybe_json(self.session.put(self.api(version, path), **kwargs))

    def maybe_json(self, result):
        try:
            return result.json()
        except ValueError as e:
            return result.text

    def api(self, version, path = None):
        if path is None:
            path = version
            version = self.version

        version = API.versions.get(version, version)
        return 'https://{}/{}{}'.format(self.server, version, path)

# An Element is a reference to an item on the server.  It does not
# contain any actual data.  Call `get` to fetch the referenced data
# from the server.
class Element(object):
    def __init__(self, api, path):
        self.api = api
        self.path = path

    def delete(self):
        return self.api.delete(self.url())

    def get(self):
        return self.api.get(self.url())

    def get_list(self, route):
        return self.api.get(self.url(route))

    def patch(self, data):
        return self.api.patch(self.url(), data)

    def post(self, route, data):
        return self.api.post(self.url(route), data)

    def put(self, data):
        return self.api.put(self.url(), data)

    # Returns a reference to a child element.
    def one(self, route, id):
        return self.one_url(self.url(route, id))

    # Returns a reference to a child collection.  Call `get_list` to
    # fetch the contents of that collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return Element(self.api, url)

    def all_url(self, url):
        return Collection(self.api, url)

    def url(self, *args):
        args = tuple([self.path] + list(args))
        return '/'.join(map(str, args))

# A Collection is a reference to a group of items on the server.  It
# does not contain any actual data.  Call `get_list` to fetch the
# referenced data from the server.
class Collection(object):
    def __init__(self, api, path):
        self.api = api
        self.path = path

    def delete(self):
        return self.api.delete(self.url())

    def get(self, id):
        return self.api.get(self.url(id))

    def get_list(self):
        return self.api.get(self.url())

    def patch(self, id, data):
        return self.api.patch(self.url(id), data)

    def post(self, data):
        return self.api.post(self.url(), data)

    def put(self, data):
        return self.api.put(self.url(data['id']), data)

    # Returns a reference to a child element.  Call `get` to fetch the
    # data instead.
    def one(self, id):
        return self.one_url(self.url(id))

    # Returns a reference to a child collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return Element(self.api, url)

    def all_url(self, url):
        return Collection(self.api, url)

    def url(self, *args):
        args = tuple([self.path] + list(args))
        return '/'.join(map(str, args))

# START HERE
class Client(object):
    default_config = {
        'salt': 'you should probably change this',
        'server': 'libraryh3lp.com',
        'timezone': 'UTC',
        'version': 'v2'
    }

    def __init__(self, profile = None):
        self.config = None
        self.api = None

        if profile:
            self.load_config(profile)

    def with_config(self, profile = None):
        self.load_config(profile)
        return self

    def load_config(self, profile = None):
        config = configparser.SafeConfigParser(Client.default_config)
        config.read([os.path.expanduser('~/.lh3/config'), os.path.expanduser('~/.lh3/credentials')])

        options = config.defaults().copy()
        options.update(dict(config.items('default')))
        if config.has_section(profile):
            options.update(dict(config.items(profile)))

        self.config = options

    def with_credentials(self, username, password = None):
        self.set_credentials(username, password)
        return self

    def set_credentials(self, username, password = None):
        self.config['username'] = username
        self.config['password'] = password

    def with_options(self, **options):
        self.config.update(options)
        return self

    def get_api(self, config = None):
        if self.api is None:
            options = self.config.copy()
            if config is not None:
                options.update(config)
            self.api = API(options)

        return self.api

    def is_admin(self):
        return self.get_api().account_id is not None

    # Returns a reference to an element.
    def one(self, route, id):
        return self.one_url(self.url(route, id))

    # Returns a reference to a collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return Element(self.get_api(), url)

    def all_url(self, url):
        return Collection(self.get_api(), url)

    def url(self, *args):
        args = tuple([''] + list(args))
        return '/'.join(map(str, args))
