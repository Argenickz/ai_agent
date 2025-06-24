import unittest
from functions.get_files_info import get_files_info

class TestCases(unittest.TestCase):
    def test_one(self):
        result = get_files_info("calculator", ".")
        print(result)

    def test_two(self):
        result = get_files_info("calculator", "pkg")
        print(result)
    def test_three(self):
        result = get_files_info("calculator", "/bin")
        print(result)
    def test_four(self):
        result = get_files_info("calculator", "../")
        print(result)


if __name__ == "__main__":
    unittest.main()