import os



def get_files_info(working_directory, directory=None):
    """This functions list all the files in a directory, this directory needs to be inside the working directory"""
    # If the directory is outside the working argument is outside the working directory, return a string with an error.

    # Let's get a hold of the working directory's absolute path
    working_dir_absolute_path = os.path.abspath(working_directory)
    print(f"working directory absolute path:\n{working_dir_absolute_path}\n")

    # Create the direcrory absolute path by joining the working directory absolute path and the directory
    directory_absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    print(f"directory absolute path:\n{directory_absolute_path}\n")

    # First check if the directory absolute path exists, if it does, check if it's outside the working directory by using the string method '.startswith()
    
    if not directory_absolute_path.startswith(working_dir_absolute_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        



def main():
    test = get_files_info("calculator", "bin")
    print(test)


if __name__ == "__main__":
    main()