import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """This function runs a python file, the file must be inside the given directory"""
    working_dir_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if file_abs_path.startswith(working_dir_abs_path):
            if os.path.exists(file_abs_path):
                if file_path.endswith(".py"):
                    arguments = ["python3", file_abs_path]
                    if args:
                        arguments.append(args)
                    answer = subprocess.run(arguments, timeout=30, capture_output=True, text=True)
                    stdout = answer.stdout
                    stderr = answer.stderr
                    format = f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
                    if answer.returncode != 0:
                        return f"{format}\nProcess exited with code {answer.returncode}"
                    if not format:
                        return 'No output produced'
                    return format
                    
                    
                return f'Error: "{file_path}" is not a Python file.'
            return f'Error: File "{file_path}" not found.'
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
def main():
    print(run_python_file("calculator", "main.py"))

if __name__=="__main__":
    main()