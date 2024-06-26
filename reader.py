from typing import List
from dataclasses import dataclass


@dataclass
class ContextManager:
    # TODO handle repos installed via github @

    path: str

    def read_file(self) -> List[List[str]]:
        try:
            with open(self.path, "r") as file:
                return list(map(self.process_line, file.readlines()))
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return []

    def process_line(self, line: str) -> List[str]:
        return line.strip().split("==")
