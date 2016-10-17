from abc import ABC, abstractmethod
import itertools
from operator import eq

equal = eq
every = lambda field, value: True

class Registry:

    _repos = {}

    @classmethod
    def register(cls, name, repo):
        cls._repos[name] = repo

    @classmethod
    def get_repo(cls, name):
        return cls._repos[name]

class Repository(ABC):

    def __init__(self, entity):
        self._entity = entity

    @abstractmethod
    def save(self, record):
        pass

    @abstractmethod
    def get(self, field, value):
        pass

    @abstractmethod
    def all(self):
        pass

    def first(self, field, value):
        found = self.get(field, value)
        try:
            first = next(itertools.islice(found, 1))
        except StopIteration:
            raise ValueError('no {} found with {}={}'.format(self._entity, field, value))
        return first

class MemoryRepository(Repository):

    def __init__(self, entity):
        super().__init__(entity)
        self._records = []
        self._next_id = 0

    def save(self, record):
        record = dict(record)
        record['id'] = self._next_id
        self._records.append(record)
        self._next_id += 1
        return record

    def get(self, field, value):
        results = []
        for rec in self._records:
            if rec[field] == value:
                results.append(rec)
        return results

    def all(self):
        return self._records
