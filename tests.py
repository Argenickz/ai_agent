import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

class TestCases(unittest.TestCase):
    def test_one(self):
        print(run_python_file("calculator", "main.py"))

    def test_two(self):
        print(run_python_file("calculator", "tests.py"))

    def test_three(self):
        print(run_python_file("calculator", "../main.py"))

    def test_four(self):
        print(run_python_file("calculator", "nonexistent.py"))


    # def test_one(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(result)

    # def test_two(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(result)

    # def test_three(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     print(result)



    # def test_one(self):
    #     result = get_files_info("calculator", ".")
    #     print(result)

    # def test_two(self):
    #     result = get_files_info("calculator", "pkg")
    #     print(result)
    # def test_three(self):
    #     result = get_files_info("calculator", "/bin")
    #     print(result)
    # def test_four(self):
    #     result = get_files_info("calculator", "../")
    #     print(result)


if __name__ == "__main__":
    unittest.main()