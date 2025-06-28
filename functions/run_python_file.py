import os

def run_python_file(working_directory, file_path):
    """This function runs a python file, the file must be inside the given directory"""
    working_dir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if file_abs_path.startswith(working_dir_abs_path):
            if os.path.exists(file_abs_path):
                if file_path.endswith(".py"):
                    return "logic goes here"
                return f'Error: "{file_path}" is not a Python file.'
            return f'Error: File "{file_path}" not found.'
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
def main():
    print(run_python_file("calculator", "main.py"))

if __name__=="__main__":
    main()