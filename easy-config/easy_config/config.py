import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Callable

import toml
import yaml
from dataclass_csv import DataclassReader, DataclassWriter

from easy_config.my_model import MyModel


class Config:

    @staticmethod
    def write_toml(path: Path, item: Any):
        path = Path(path).with_suffix('.toml')
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _to_dict(item)
        with path.open('w') as _:
            toml.dump(data, _)

    @staticmethod
    def read_toml[T](path: Path, loader: Callable[[dict], T]) -> T:
        path = Path(path).with_suffix('.toml')
        with path.open() as _:
            data = toml.load(_)
            return loader(data)

    @staticmethod
    def write(path: Path, item: Any):
        path = Path(path).with_suffix('.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _to_dict(item)
        with path.open('w') as _:
            json.dump(data, _, indent=2)

    @staticmethod
    def read[T](path: Path, loader: Callable[[dict], T]) -> T:
        path = Path(path).with_suffix('.json')
        with path.open() as _:
            data = json.load(_)
            return loader(**data)

    @staticmethod
    def write_yaml(path: Path, item: Any):
        path = Path(path).with_suffix('.yaml')
        path.parent.mkdir(parents=True, exist_ok=True)
        data = _to_dict(item)
        with path.open('w') as _:
            yaml.dump(data, _, indent=2)

    @staticmethod
    def read_yaml[T](path: Path, loader: Callable[[dict], T]) -> T:
        path = Path(path).with_suffix('.yaml')
        with path.open() as _:
            data = yaml.safe_load(_)
            return loader(data)

    @staticmethod
    def write_csv[T](path: Path, data: list[T]):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as _:
            w = DataclassWriter(_, data, data[0].__class__)
            w.write()

    @staticmethod
    def read_csv[T](path: Path, _type: T) -> list[T]:
        with path.open() as _:
            reader = DataclassReader(_, _type)
            return [_ for _ in reader]


def _to_dict(item: Any):
    if is_dataclass(item):
        return asdict(item)
    match item:
        case MyModel():
            return item.to_dict()
    raise NotImplementedError(f'{type(item)}')
