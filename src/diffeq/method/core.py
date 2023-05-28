from typing import Any, NamedTuple, Callable, List
from diffeq.core import Point
from diffeq.report.table import Table


class MethodInput(NamedTuple):
    f: Callable[[float, float], float]
    start: Point
    x_limit: float
    step: float
    eps: float

    @property
    def validated(self) -> 'MethodInput':
        assert 0 < self.step
        assert self.start.x < self.x_limit
        assert 0 < self.eps
        return self


class MethodOutput(NamedTuple):
    points: List[Point]
    table: Table


OneStepMethod = Callable[[MethodInput], MethodOutput]
