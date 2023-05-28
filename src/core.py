from typing import Callable


class Function2:
    def __init__(self, string: str, callable: Callable[[float, float], float]):
        self.__string = string
        self.__origin = callable

    def __str__(self) -> str:
        return self.__string

    def __call__(self, *args: float) -> float:
        return self.__origin(*args)


class FirstOrderEquation:
    def __init__(self, f: Function2):
        self.f = f

    def __str__(self) -> str:
        return f'dy/dx = {self.f}'
