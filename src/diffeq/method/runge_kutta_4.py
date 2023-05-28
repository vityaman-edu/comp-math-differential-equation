from diffeq.core import Point
from diffeq.report.table import Table
from diffeq.method.core import (
    MethodInput as Input,
    MethodOutput as Output,
)


def solve(input: Input) -> Output:
    '''
    https://ru.wikipedia.org/wiki/Метод_Рунге_—_Кутты
    '''

    f, (x_0, y_0), x_n, h = input.validated

    def k_1(x: float, y: float) -> float:
        return f(x, y)

    def k_2(x: float, y: float) -> float:
        return f(x + h / 2, y + h * k_1(x, y) / 2)

    def k_3(x: float, y: float) -> float:
        return f(x + h / 2, y + h * k_2(x, y) / 2)

    def k_4(x: float, y: float) -> float:
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

    return Output(
        list(map(lambda t: Point(*t), zip(x, y))),  # type: ignore
        Table(
            ['i', 'x', 'y', 'k1', 'k2', 'k3', 'k4'],
            list(zip(range(len(x)), x, y, k1, k2, k3, k4))
        )
    )
