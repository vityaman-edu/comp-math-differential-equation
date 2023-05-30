from typing import Any, Iterable, NamedTuple


class Point(NamedTuple):
    x: float
    y: float


def partition(left: float, right: float, h: float) -> Iterable[float]:
    assert left < right
    assert h > 0
    x = left
    while x <= right:
        yield x
        x += h


class Line(NamedTuple):
    k: float
    b: float
    
    def __call__(self, x: float) -> float:
        return self.k * x + self.b

    @classmethod
    def between(cls, a: Point, b: Point) -> 'Line':
        m = (b.y - a.y) / (b.x - a.x)
        return Line(k = m, b = -m * a.x + a.y)
