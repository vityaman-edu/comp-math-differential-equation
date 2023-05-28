from diffeq.core import Point
from diffeq.report.table import Table
from diffeq.method.core import (
    MethodInput as Input,
    MethodOutput as Output,
)


def solve(input: Input, corrected: bool = True) -> Output:
    '''
    Частный случай неявного метода Рунге-Кутты.

    https://ru.wikipedia.org/wiki/Метод_Эйлера
    https://ru.wikipedia.org/wiki/Метод_Рунге_—_Кутты
    '''

    f, (x_0, y_0), x_n, h = input.validated

    x = [x_0]
    y = [y_0]
    while x[-1] <= x_n:
        x += [x[-1] + h]
        y += [y[-1] + (x[-1] - x[-2]) * f(x[-2], y[-1])]
        if corrected:
            y[-1] = y[-2] \
                + (x[-1] - x[-2]) \
                * (f(x[-2], y[-2]) + f(x[-1], y[-1])) / 2

    return Output(
        list(map(lambda t: Point(*t), zip(x, y))), # type: ignore
        Table(
            ['i', 'x', 'y'],
            list(zip(range(len(x)), x, y)),
        ),
    )
