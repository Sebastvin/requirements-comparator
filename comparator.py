from typing import List
from dataclasses import dataclass


@dataclass
class Comparator:
    requirements_first: List[List[str]]
    requirements_second: List[List[str]]

    def compare(self):
        ...

    def process(self):
        ...

    def results(self):
        ...

    def __str__(self) -> None:
        return self.__class__.__name__
