from typing import Any, NamedTuple, Callable, List
from diffeq.core import Point, Line
from diffeq.report.table import Table
from bisect import bisect_left, bisect_right


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
    h: float
    
    @property
    def f(self) -> Callable[[float], float]:
        x = list(map(lambda p: p.x, self.points))
        def at(arg: float) -> float:
            i = bisect_left(x, arg) - 1
            if i == len(x) - 2:
                return self.points[i + 1].y
            line = Line.between(self.points[i], self.points[i + 1])
            return line(arg)
        return at


OneStepMethod = Callable[[MethodInput], MethodOutput]
