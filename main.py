from reader import ContextManager
from comparator import Comparator

if __name__ == "__main__":
    ct = ContextManager("requirements_first.txt")

    result = ct.read_file()
    c = Comparator(result, result)

    print(c.compare())
