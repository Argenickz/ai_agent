from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_files import write_file
from functions.run_python import run_python
import unittest

class TestGetFilesInfo(unittest.TestCase):
    def test_one(self):
        print(run_python('calculator', 'main.py'))
    
    def test_two(self):
        print(run_python('calculator', 'tests.py'))

    def test_three(self):
        print(run_python('calculator', '../main.py'))
    
    def test_four(self):
        print(run_python('calculator', 'nonexistent.py'))
    # def test_one(self):
    #     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    #     print(result)
    
    # def test_two(self):
    #     result = write_file("calculator", "pgk/morelorem.txt", "lorem ipsum dolor sit amet")
    #     print(result)

    # def test_three(self):
    #     result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #     print(result)

    # def test_files(self):
    #     report = get_file_content("calculator", "main.py")
    #     print(report)

    # def test_files2(self):
    #     report2 = get_file_content("calculator", "pkg/calculator.py")
    #     print(report2)
    # def test_files3(self):
    #     report3 = get_file_content("calculator", "/bin/cat")
    #     print(report3)
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