from typing import Tuple
from diffeq.core import Point
from diffeq.report.table import Table
from diffeq.method.runge import runge_rule
from diffeq.method.core import (
    MethodInput as Input,
    MethodOutput as Output,
    OneStepMethod,
)


def solve(input: Input, one_step: OneStepMethod) -> Output:
    '''
    Метод Милна относится к многошаговым методам и представляет 
    один из методов прогноза и коррекции.

    Для получения формул Милна используется первая интерполяционная 
    формула Ньютона с разностями до третьего порядка.

    Для начала счета требуется задать решения в трех первых точках, 
    которые можно получить одношаговыми методами (например, 
    методом Рунге-Кутта).
    '''

    f, (x_0, y_0), x_n, h, eps = input.validated

    p = 4 # Порядок точности

    # Compute first 3 points
    (points, _, h) = one_step(Input(f, Point(x_0, y_0), x_0 + 3 * h, h, eps))

    def next(h: float) -> Tuple[float, float, float, float]:
        x_i = x[-1] + h
        y_i_predict = y[-4] + 4 / 3 * h * (
            + 2 * f(x[-3], y[-3])
            - f(x[-2], y[-2])
            + 2 * f(x[-1], y[-1])
        )
        f_i_predict = f(x_i, y_i_predict)
        y_i_correct = y[-2] + h / 3 * (
            + f(x[-2], y[-2])
            + 4 * f(x[-1], y[-1])
            + f_i_predict
        )
        while abs(y_i_predict - y_i_correct) > eps:
            y_i_predict = y_i_correct
            f_i_predict = f(x_i, y_i_predict)
            y_i_correct = y[-2] + h / 3 * (
                + f(x[-2], y[-2])
                + 4 * f(x[-1], y[-1])
                + f_i_predict
            )   
        return (x_i, y_i_predict, f_i_predict, y_i_correct)

    x = list(map(lambda p: p.x, points))
    y = y_predict = list(map(lambda p: p.y, points))
    y_correct = list(map(lambda p: p.y, points))
    f_predict = [f(x, y) for x, y in zip(x, y)]
    while abs(x[-1] - x_n) >= h / 2:
        x_i, y_i_predict, f_i_predict, y_i_correct = next(h)
        
        y_predict += [y_i_predict]
        y_correct += [y_i_correct]
        f_predict += [f_i_predict]
        x += [x_i]

    return Output(
        list(map(lambda t: Point(*t), zip(x, y))),  # type: ignore
        Table(
            ['i', 'x', 'y_c', 'y_p', 'f_p'],
            list(zip(
                range(len(x)),
                x,
                y,
                y_predict,
                f_predict,
            )),
        ),
        h = h
    )
