from typing import List
from dataclasses import dataclass
from src.models.schemas import Package


@dataclass
class ContextManager:
    path: str

    def read_file(self) -> List[List[str]]:
        try:
            with open(self.path, "r") as file:
                return list(map(self.process_line, file.readlines()))
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return []

    def process_line(self, line: str) -> Package:
        line = line.strip()
        if not line or line.startswith("#"):
            return None

        # Handle Git repository packages
        if "@" in line and "git+" in line:
            parts = line.split("@")
            name = parts[0].strip()
            return Package(name=name, version="")

        # Handle regular packages with versions
        if "==" in line:
            name, version = line.split("==")
            return Package(name=name.strip(), version=version.strip())

        return Package(name=line, version="")
