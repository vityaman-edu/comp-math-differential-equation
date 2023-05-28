from typing import Any, NamedTuple, Callable, List
from diffeq.core import Point
from diffeq.report.table import Table


class MethodInput(NamedTuple):
    f: Callable[[float, float], float]
    start: Point
    x_limit: float
    step: float

    @property
    def validated(self) -> 'MethodInput':
        assert self.step > 0
        assert self.start.x < self.x_limit
        return self


class MethodOutput(NamedTuple):
    points: List[Point]
    table: Table


OneStepMethod = Callable[[MethodInput], MethodOutput]
