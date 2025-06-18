from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
import unittest

class TestGetFilesInfo(unittest.TestCase):
    def test_files(self):
        report = get_file_content("calculator", "main.py")
        print(report)

    def test_files2(self):
        report2 = get_file_content("calculator", "pkg/calculator.py")
        print(report2)
    def test_files3(self):
        report3 = get_file_content("calculator", "/bin/cat")
        print(report3)
    # def test_one(self):
    #     report = get_files_info("calculator", ".")
    #     print(report)

    # def test_two(self):
    #     report = get_files_info("calculator", "pkg")
    #     print(report)

    # def test_three(self):
    #     report = get_files_info("calculator", "/bin")
    #     print(report)

    # def test_four(self):
    #     report = get_files_info("calculator", "..")
    #     print(report)




if __name__ == "__main__":
    unittest.main()