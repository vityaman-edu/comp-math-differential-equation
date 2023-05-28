from typing import NamedTuple
from core import FirstOrderEquation


class Input(NamedTuple):
    eq: FirstOrderEquation
    x_0: float
    y_0: float
    x_n: float
    h: float
    corrected: bool

    def valid(self) -> 'Input':
        assert self.h > 0
        assert self.x_0 < self.x_n
        return self


class Output(NamedTuple):
    x: list[float]
    y: list[float]

    @property
    def n(self) -> int:
        return len(self.x)


def solve(input: Input) -> Output:
    '''
    Частный случай неявного метода Рунге-Кутты.
    
    https://ru.wikipedia.org/wiki/Метод_Эйлера
    https://ru.wikipedia.org/wiki/Метод_Рунге_—_Кутты
    '''

    eq, x_0, y_0, x_n, h, corrected = input.valid()
    f = eq.f

    x = [x_0]
    y = [y_0]
    while x[-1] <= x_n:
        x += [x[-1] + h]
        y += [y[-1] + (x[-1] - x[-2]) * f(x[-2], y[-1])]
        if corrected:
            y[-1] = y[-2] \
                + (x[-1] - x[-2]) \
                * (f(x[-2], y[-2]) + f(x[-1], y[-1])) / 2

    return Output(x, y)
