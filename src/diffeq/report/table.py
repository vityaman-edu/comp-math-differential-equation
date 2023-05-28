from typing import Any, NamedTuple, List, Callable, Tuple
from tabulate import tabulate


class Table(NamedTuple):
    headers: List[str]
    rows: List[Tuple[Any, ...]]


TableConsumer = Callable[[Table], None]


class TabulatePrinter:
    def __init__(self, tablefmt: str) -> None:
        self.tablefmt = tablefmt

    def __call__(self, table: Table) -> None:
        print(tabulate(
            tabular_data=table.rows,
            headers=table.headers,
            tablefmt=self.tablefmt
        ))
