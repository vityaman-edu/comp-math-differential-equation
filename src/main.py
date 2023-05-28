import matplotlib.pyplot as plt
from math import *
from typing import List
from core import *
from diffeq.core import Point
from diffeq.method.euler import solve as solve_euler
from diffeq.method.runge_kutta_4 import solve as solve_runge_kutta_4
from diffeq.method.milne import solve as solve_milne
from diffeq.method.core import MethodInput as Input, OneStepMethod
from diffeq.report.table import TabulatePrinter


if __name__ == '__main__':
    results = [
        None,
        lambda x: 2 * exp(-2 * x),
        lambda x: log(exp(x ** 2) + 1),
    ]
    equations = [
        ('y + (1 + x) * y ^ 2', lambda x, y: y + (1 + x) * y ** 2),

        # C * exp(-2 * x), 0 2 4
        ('-2 * y', lambda x, y: -2 * y),

        # y = ln(exp(x ** 2) + 1),
        ('2 * x * exp(x ** 2) / (exp(x ** 2) + 1)', lambda x,
         y: 2 * x * exp(x ** 2) / (exp(x ** 2) + 1)),
    ]
    equations = list(map(
        lambda args: FirstOrderEquation(Function2(*args)),  # type: ignore
        equations
    ))

    method_names = [
        'Basic Euler',
        'Corrected Euler',
        'Runge-Kutta 4',
        'Milne',
    ]

    methods: List[OneStepMethod] = [
        lambda args: solve_euler(args, corrected=False),
        lambda args: solve_euler(args, corrected=True),
        lambda args: solve_runge_kutta_4(args),
        lambda args: solve_milne(
            args, lambda args: solve_runge_kutta_4(args, runge=True)),
    ]

    def print_table(x): return None

    # print_table = TabulatePrinter(
    #     tablefmt='simple_grid'
    # )

    print(
        f'=== Welcome to differential eqsolver ===',
        f'',
        f'Here you can solve differential equations using:',
        *tuple(map(lambda name: f'- {name}', method_names)),
        f'',
        f'Choice a one of first-order equations:',
        *list(map(lambda t: f'[{t[0]}]: {t[1]}',
                  enumerate(map(str, equations)))),
        sep='\n'
    )

    propmt = f'Enter a number of equation i in [0..{len(equations) - 1}]: '
    eq_index = int(input(propmt))
    eq = equations[eq_index]

    print(f'Taken: {eq}')

    print(f'Enter boundaties: ')
    x_0 = float(input('Enter x_0: '))
    y_0 = float(input('Enter y_0: '))
    x_n = float(input('Enter x_n: '))
    h = float(input('Enter h: '))
    eps = float(input('Enter eps: '))
    print()
    print('Input parameters: ')
    print(f'> x_0 = {x_0}')
    print(f'> y_0 = {y_0}')
    print(f'> x_n = {x_n}')
    print(f'> h   = {h}')
    print(f'> eps = {eps}')
    print()
    print('Enjoy results!')
    print()

    args = Input(eq.f, Point(x_0, y_0), x_n, h, eps)  # type: ignore

    for name, method in zip(method_names, methods):
        out = method(args)
        print(f'=== Report of {name} === ')
        print_table(out.table)
        print()
        print(f"Result of {name} is {out.points[-1].y}")
        print(f"Total iterations: {len(out.points)}")
        print(f"Stop at: {out.points[-1].x}")
        print()

        if name == method_names[2]:
            x = list(map(lambda p: p.x, out.points))
            y = list(map(lambda p: p.y, out.points))
            if eq_index != 0:
                plt.plot(x, y, x, list(map(results[eq_index], x)))
                plt.show()
