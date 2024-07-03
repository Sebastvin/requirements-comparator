from reader import ContextManager
from comparator import Comparator

if __name__ == "__main__":
    ct_first = ContextManager("requirements_first.txt")
    ct_second = ContextManager("requirements_second.txt")

    result_first = ct_first.read_file()
    result_second = ct_second.read_file()

    c = Comparator(result_first, result_second)

    print(c.compare())
