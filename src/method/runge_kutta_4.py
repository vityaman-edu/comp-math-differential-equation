from typing import NamedTuple
from core import FirstOrderEquation


class Input(NamedTuple):
    eq: FirstOrderEquation
    x_0: float
    y_0: float
    x_n: float
    h: float

    def valid(self) -> 'Input':
        assert self.h > 0
        assert self.x_0 < self.x_n
        return self


class Output(NamedTuple):
    x: list[float]
    y: list[float]
    k1: list[float]
    k2: list[float]
    k3: list[float]
    k4: list[float]

    @property
    def n(self) -> int:
        return len(self.x)


def solve(input: Input) -> Output:
    '''
    https://ru.wikipedia.org/wiki/Метод_Рунге_—_Кутты
    '''

    eq, x_0, y_0, x_n, h = input.valid()
    f = eq.f

    def k_1(x, y):
        return f(x, y)

    def k_2(x, y):
        return f(x + h / 2, y + h * k_1(x, y) / 2)

    def k_3(x, y):
        return f(x + h / 2, y + h * k_2(x, y) / 2)

    def k_4(x, y):
        return f(x + h, y + h * k_3(x, y))

    x, y = [x_0], [y_0]
    k1, k2, k3, k4 = [], [], [], []
    while x[-1] < x_n + h:
        k1 += [k_1(x[-1], y[-1])]
        k2 += [k_2(x[-1], y[-1])]
        k3 += [k_3(x[-1], y[-1])]
        k4 += [k_4(x[-1], y[-1])]
        y += [y[-1] + h / 6
              * (k1[-1] + 2 * k2[-1] + 2 * k3[-1] + k4[-1])]
        x += [x[-1] + h]
    return Output(x, y, k1, k2, k3, k4)
