from typing import List, Dict
from dataclasses import dataclass
from schemas import Package


@dataclass
class Comparator:
    requirements_first: List[Package]
    requirements_second: List[Package]

    def compare(self) -> Dict[str, List]:
        same_values = []
        different_values = []
        only_in_first = []
        only_in_second = []

        first_dict = {pkg.name: pkg for pkg in self.requirements_first}
        second_dict = {pkg.name: pkg for pkg in self.requirements_second}

        all_packages = set(first_dict) | set(second_dict)

        for pkg_name in all_packages:
            if pkg_name in first_dict and pkg_name in second_dict:
                pkg1, pkg2 = first_dict[pkg_name], second_dict[pkg_name]
                if pkg1.version == pkg2.version:
                    same_values.append(pkg1)
                else:
                    different_values.append((pkg1, pkg2))
            elif pkg_name in first_dict:
                only_in_first.append(first_dict[pkg_name])
            else:
                only_in_second.append(second_dict[pkg_name])

        return {
            "same": same_values,
            "different": different_values,
            "only_in_first": only_in_first,
            "only_in_second": only_in_second,
        }

    def process(self):
        ...

    def results(self):
        ...

    def __str__(self) -> None:
        return self.__class__.__name__
