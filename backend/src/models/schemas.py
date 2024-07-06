from pydantic import BaseModel
from typing import List, Tuple


class Package(BaseModel):
    name: str
    version: str


class ComparisonResult(BaseModel):
    same: List[Package]
    different: List[Tuple[Package, Package]]
    only_in_first: List[Package]
    only_in_second: List[Package]
