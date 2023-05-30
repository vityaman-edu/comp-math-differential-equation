from typing import Tuple
from diffeq.core import Point
from diffeq.report.table import Table
from diffeq.method.core import (
    MethodInput as Input,
    MethodOutput as Output,
)
from diffeq.method.runge import runge_rule


def solve(input: Input, corrected: bool = True) -> Output:
    '''
    Частный случай неявного метода Рунге-Кутты.

    https://ru.wikipedia.org/wiki/Метод_Эйлера
    https://ru.wikipedia.org/wiki/Метод_Рунге_—_Кутты
    '''

    f, (x_0, y_0), x_n, h, eps = input.validated

    p = 2 if corrected else 1  # Порядок точности

    def next(h: float) -> Tuple[float, float]:
        x_i = x[-1] + h
        y_i = y[-1] + (x_i - x[-1]) * f(x[-1], y[-1])
        return (x_i, y_i)

    def correct(x_i: float, y_i: float) -> Tuple[float, float]:
        y_i = y[-1] + (x_i - x[-1]) * (
            f(x[-1], y[-1]) + f(x_i, y_i)
        ) / 2
        return (x_i, y_i)

    x = [x_0]
    y = [y_0]
    while abs(x[-1] - x_n) >= h / 2:
        x_i, y_i = next(h)


        x_i_half, y_i_half = next(h / 2)
        x += [x_i_half]; y += [y_i_half]
        x_i_half, y_i_half = next(h / 2)
        x.pop(); y.pop()

        if corrected:
            x_i, y_i = correct(x_i, y_i)
            x_i_half, y_i_half = correct(x_i_half, y_i_half)

        if not runge_rule(y_i, y_i_half, p, eps):
            h /= 2
            continue

        x += [x_i]
        y += [y_i]

    return Output(
        list(map(lambda t: Point(*t), zip(x, y))),  # type: ignore
        Table(
            ['i', 'x', 'y'],
            list(zip(range(len(x)), x, y)),
        ),
        h = h
    )
