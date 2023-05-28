from tabulate import tabulate
from typing import NamedTuple
from core import *
import method.euler
import method.runge_kutta_4


class App(NamedTuple):
    equations: list[FirstOrderEquation]

    def run(self) -> None:
        self.__welcome()
        eq_index = self.__promt_eq_index()
        self.__one_step(eq_index)

    def __welcome(self) -> None:
        print(
            f'=== Welcome to differential eqsolver ===',
            f'Here you can solve differential equations using:',
            f'- Euler\'s method',
            f'- Corrected Euler\'s method',
            f'- Runge-Kutta 4',
            f'Choice a one of first-order equations:',
            *list(map(lambda t: f'[{t[0]}]: {t[1]}',
                  enumerate(map(str, self.equations)))),
            sep='\n'
        )

    def __promt_eq_index(self) -> int:
        while True:
            eq_index_max = len(self.equations) - 1
            index_expectation = f'i in [0..{eq_index_max}]'
            text = input(f'Enter a number of equation {index_expectation}: ')
            eq_index = int(text) if text.isdigit() else -1
            if 0 <= eq_index <= eq_index_max:
                return eq_index
            print(
                f'You typed a wrong answer, got \'{text}\', '
                f'but expected {index_expectation}'
            )

    def __one_step(self, eq_index: int) -> None:
        print(f'Enter Euler\'s input:')

        eq = self.equations[eq_index]
        x_0 = float(input('Enter x_0: '))
        y_0 = float(input('Enter y_0: '))
        x_n = float(input('Enter x_n: '))
        h = float(input('Enter h: '))

        print('Enjoy!')

        out_basic = method.euler.solve(method.euler.Input(
            eq, x_0, y_0, x_n, h, corrected=False
        ))

        out_corrected = method.euler.solve(method.euler.Input(
            eq, x_0, y_0, x_n, h, corrected=True
        ))

        out_kutta = method.runge_kutta_4.solve(
            method.runge_kutta_4.Input(
                eq, x_0, y_0, x_n, h
            )
        )

        def report_euler(title: str, out: method.euler.Output) -> None:
            print(f'=== Report of {title} ===')
            print(tabulate(
                list(zip(range(0, out.n), out.x, out.y)),
                headers=('i', 'x', 'y'),
                tablefmt='simple_grid'
            ))
            print()

        report_euler('Basic Euler', out_basic)
        report_euler('Corrected Euler', out_corrected)

        print(f'=== Report of Runge-Kutta 4 ===')
        print(tabulate(
            list(zip(
                range(0, out_kutta.n),
                out_kutta.x, 
                out_kutta.y,
                out_kutta.k1,
                out_kutta.k2,
                out_kutta.k3,
                out_kutta.k4,
            )),
            headers=('i', 'x', 'y', 'k1', 'k2', 'k3', 'k4'),
            tablefmt='simple_grid',
        ))
        print()
