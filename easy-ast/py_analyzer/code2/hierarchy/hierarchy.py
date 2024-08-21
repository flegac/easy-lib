from typing import Iterable, Self
from unittest import TestCase

from pydantic import BaseModel, Field


class Hierarchy(BaseModel):
    hierarchy: dict[str, dict] = Field(default_factory=dict)
    splitter: str = '.'

    def union(self, other: Self):
        keys = set(self.hierarchy).union(other.hierarchy)

        xxx = self.hierarchy | other.hierarchy

        data = {
            Hierarchy(hierarchy=None)
            for k in keys
        }

        res = Hierarchy(hierarchy={

        })

    def difference(self, other: Self):
        raise NotImplemented

    def is_present(self, name: str):
        parts = name.split(self.splitter)
        lookup = self.hierarchy
        for part in parts:
            if part not in lookup:
                return False
            lookup = lookup[part]
        return True

    def register(self, path: str):
        hierarchy = self.hierarchy

        for part in path.split(self.splitter):
            if part not in hierarchy:
                hierarchy[part] = {}
            hierarchy = hierarchy[part]

    def load_all(self, items: Iterable[str]):
        for _ in items:
            self.register(_)
        return self

    def remove_all(self, packages: set[str]):
        for _ in packages:
            self.hierarchy.pop(_, None)

    def keep_only(self, packages: set[str]):
        to_remove = set(filter(lambda x: x not in packages, self.hierarchy.keys()))
        self.remove_all(to_remove)

    def clear(self):
        self.hierarchy.clear()

    def _full_names(self, hierarchy: dict[str, dict], prefix: str = None):
        res = set()
        if prefix is not None:
            res.add(prefix)
        for name, sub in hierarchy.items():
            base = '.'.join([prefix, name]) if prefix is not None else name
            res.update(self._full_names(hierarchy=sub, prefix=base))
        return res

    def iter(self):
        return self._full_names(self.hierarchy)


class RecursiveSet:

    @staticmethod
    def union(a: str | set | dict, b: str | set | dict) -> dict:
        a = RecursiveSet.to_dict(a)
        b = RecursiveSet.to_dict(b)
        return {
            k: RecursiveSet.union(a.get(k, {}), b.get(k, {}))
            for k in set(a.keys()).union(b.keys())
        }

    @staticmethod
    def to_dict(data: str | set | dict):
        match data:
            case str():
                return {data}
            case set():
                return data
            case dict():
                return data
            case None:
                return data
        raise NotImplementedError(f'{type(data)}')


class TestRecursiveSet(TestCase):
    def test_union(self):
        a = {'a': 'b'}
        b = {'b': 'c'}

        expected = {
            'a': 'b',
            'b': 'c'
        }

        actual = RecursiveSet.union(a, b)
        self.assertDictEqual(expected, actual)
