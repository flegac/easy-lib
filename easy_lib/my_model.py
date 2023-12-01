from typing import Any

from pydantic import BaseModel, Extra


class MyModel(BaseModel):
    class Config:
        extra = Extra.forbid

    def to_dict(self):
        return self.model_dump()

    def clone(self, update: dict[str, Any] = None):
        item = self.model_dump()
        if update is not None:
            for key, value in update.items():
                self._my_update(item, key, value)
        return type(self)(**item)

    @staticmethod
    def _my_update(target: dict, path: str, value: Any):
        if '.' not in path:
            target[path] = value
        else:
            parts = path.split('.')
            for key in parts[:-1]:
                target = target[key]
            target[parts[-1]] = value
