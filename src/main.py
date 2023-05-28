from core import *
from app import App

# mypy: ignore-errors
if __name__ == '__main__':
    equations = [
        ('y + (1 + x) * y ^ 2', lambda x, y: y + (1 + x) * y ** 2),
    ]
    equations = list(map(
        lambda args: FirstOrderEquation(Function2(*args)), 
        equations
    ))
    App(equations).run()
