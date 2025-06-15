from functions.get_files_info import get_files_info
import unittest

class TestGetFilesInfo(unittest.TestCase):
    def test_one(self):
        report = get_files_info("calculator", ".")
        print(report)

    def test_two(self):
        report = get_files_info("calculator", "pkg")
        print(report)

    def test_three(self):
        report = get_files_info("calculator", "/bin")
        print(report)

    def test_four(self):
        report = get_files_info("calculator", "..")
        print(report)




if __name__ == "__main__":
    unittest.main()