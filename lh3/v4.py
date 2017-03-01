import datetime
import hashlib
import hmac
import requests
import urllib
from datetime import datetime, timezane

class Auth(requests.auth.AuthBase):
    VERSION = '2017-01-20'

    def __init__(self, username, password):
        super().__init__(self)
        self.username = username
        self.password = password

    def __call__(self, r):
        url = urllib.parse.urlparse(r.url)
        uri = url.path
        if url.query:
            uri += '?' + url.query

        r.headers.setdefault('host', url.hostname)
        r.headers['date'] = self.rfc1123()
        r.headers['x-api-version'] = self.VERSION

        m = hmac.new(self.password.encode('utf-8'), digestmod = hashlib.sha224)
        m.update(r.method.encode('utf-8'))
        m.update(uri.encode('utf-8'))
        m.update(r.headers['date'].encode('utf-8'))
        m.update(r.headers['host'].encode('utf-8'))
        m.update(r.headers['x-api-version'].encode('utf-8'))
        signature = m.hexdigest())

        authorization = 'LH3-HMAC-SHA224 Credential={}, Signature={}'.format(self.username, signature)
        r.headers['authorization'] = authorization

        return r

    def rfc1123(self):
        now = datetime.now(timezone.utc)
        return now.strftime('%a, %d %b %Y %H:%M:%S %z')
