from __future__ import unicode_literals
from builtins import object

class Resource(object):
    id = 'id'

    def __init__(self, endpoint, data = None):
        self._endpoint = endpoint
        self._data = data
        self._changes = {}
        if not self._data:
            self.read()

    def __getattr__(self, name):
        if name in self._changes:
            return self._changes[name]
        else:
            return self._data.get(name)

    def __setattr__(self, name, value):
        self._changes[name] = value

    def read(self):
        self._data = self._endpoint.get()
        self._changes = {}

    def update(self):
        if self._changes:
            self._endpoint.put(self._changes)
            for key in self._changes:
                self._data[key] = self._changes[key]

    def delete(self):
        self._endpoint.delete()

class Collection(object):
    def __init__(self, resource, endpoint, items = None):
        self._resource = resource
        self._endpoint = endpoint
        self._items = items
        if not self._items:
            self.list()

    def __len__(self):
        return len(self._items)

    def __getattr__(self, index):
        return self.items[index]

    def list(self):
        records = self._endpoint().get_list()
        self._items = []
        for record in records:
            endpoint = self._endpoint.one(record[self.resource.id])
            item = self._resource(endpoint, record)
            self.items.append(item)

    def create(self, data):
        record = self._endpoint.post(data)
        data.update(record)
        endpoint = self._endpoint.one(record[self.resource.id])
        item = self._resource(endpoint, record, data)
        self._items.append(item)
        return item
