import inspect
import statistics
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable
from unittest import TestCase

from loguru import logger

HEADERS = ['label', 'total (s)', 'count', 'min', 'max', 'mean', 'std']


@dataclass
class TimeEntry:
    events: list[float] = field(default_factory=list)

    def raw_line(self, key: str):
        return [key, self.total, self.count, self.min, self.max, self.mean, self.std]

    @property
    def total(self):
        return sum(self.events)

    @property
    def count(self):
        return len(self.events)

    @property
    def min(self):
        return self._undefined(min(self.events))

    @property
    def max(self):
        return self._undefined(max(self.events))

    @property
    def mean(self):
        return self._undefined(statistics.mean(self.events))

    @property
    def std(self):
        return self._undefined(statistics.pstdev(self.events))

    def _undefined(self, value: float):
        if len(self.events) <= 1:
            return ''
        return value


class Timings:
    def __init__(self):
        self.db: dict[str, TimeEntry] = defaultdict(lambda: TimeEntry())
        self.active = False
        self.logs = False

    @contextmanager
    def timing(self, name: str = None):
        if name is None:
            name = inspect.stack()[11].function
        start = self._before(name)
        yield
        self._after(name, start)

    def time_func[** P, R](self, func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            with self.timing(func.__qualname__):
                return func(*args, **kwargs)

        return inner

    def show_timing(self):

        groups = {}

        for key, entry in self.db.items():
            try:
                major, minor = key.split('.', maxsplit=1)
            except:
                major = '___'
                minor = key
            if major not in groups:
                groups[major] = {}
            groups[major][minor] = entry

        if not self.active:
            return
        try:
            from tabulate import tabulate
            from numpy import average

            logger.info('\n' + tabulate(
                headers=HEADERS,
                floatfmt='.5f',
                tabular_data=sorted([
                    entry.raw_line(key)
                    for key, entry in self.db.items()
                ], key=lambda row: row[1], reverse=True),
            )
                        )
        except Exception as e:
            logger.warning(f'Warning: {e}')

    def setup_timing(self, status: bool = True, logs: bool = False):
        self.active = status
        self.logs = logs

    def _before(self, name: str):
        if self.logs:
            logger.debug(f'+ {name}')
        if self.active:
            return time.time()

    def _after(self, name: str, start: float | None):
        if self.logs:
            logger.debug(f'- {name}')
        if start is not None:
            total = time.time() - start
            self.db[name].events.append(total)


_TIMING = Timings()
timing = _TIMING.timing
time_func = _TIMING.time_func
show_timing = _TIMING.show_timing
setup_timing = _TIMING.setup_timing


class TimingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        setup_timing()

    @classmethod
    def tearDownClass(cls):
        show_timing()
