import random

from easy_config.my_model import MyModel


class Position(MyModel):
    x: float = 0
    y: float = 0

    @staticmethod
    def random():
        return Position(x=random.random(), y=random.random())

    @staticmethod
    def from_raw(y: float, x: float):
        return Position(x=x, y=y)

    def raw(self):
        return self.y, self.x
