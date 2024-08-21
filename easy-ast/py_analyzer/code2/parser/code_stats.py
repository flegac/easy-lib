from collections import defaultdict
from typing import Self

from pydantic import BaseModel, Field


class CodeStats(BaseModel):
    modules: set[str] = Field(default_factory=set)
    classes: set[str] = Field(default_factory=set)
    functions: set[str] = Field(default_factory=set)

    others: dict[str, set[str]] = Field(default_factory=lambda: defaultdict(set))

    @property
    def imports(self):
        return self.others['imports']

    @property
    def func_calls(self):
        return self.others['func_calls']

    @property
    def assignments(self):
        return self.others['assignments']

    @property
    def loops(self):
        return self.others['loops']

    @property
    def conditions(self):
        return self.others['conditions']

    @property
    def variables(self):
        return self.others['variables']

    @property
    def constants(self):
        return self.others['constants']

    def iter_all(self):
        for _ in self.imports:
            yield _

        for _ in self.modules:
            yield _
        for _ in self.classes:
            yield _
        for _ in self.functions:
            yield _

    def load(self, other: Self):
        self.modules.update(other.modules)
        self.classes.update(other.classes)
        self.functions.update(other.functions)

        for k, values in other.others.items():
            self.others[k].update(values)

    def __repr__(self):
        code = f'modules:{len(self.modules)}, cls:{len(self.classes):2}, fun:{len(self.functions):2}'
        stats = f'import:{len(self.imports):3}, calls:{len(self.func_calls):3}, const:{len(self.constants):4}'
        stats2 = f'loop:{len(self.loops):2}, cond:{len(self.conditions):3}, assign:{len(self.assignments):4}'
        return f'{code}\n{stats}\n{stats2}'

    def __str__(self):
        return repr(self)

    def print_debug(self):
        print(self)
        print('class', self.classes)
        print('func', self.functions)
        print('call', self.func_calls)
        print('const', self.constants)
        print('loops', self.loops)
        print('conditions', self.conditions)
        print('assignments', self.assignments)
