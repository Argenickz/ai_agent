import os
import subprocess
"""
! Run Python
It's time to build the functionality for our Agent to run arbitrary code in Python.

Now, it's worth pausing to point out the inherent security risks here. We have a few things going for us:
    1. We'll only allow the LLM to run code in a specific directory(the working_directory).
    2. We'll use a 30 second timeout to prevent it from running indefinitely.

But aside from that... yes, the LLM can run arbitrary code that we(or it) places in the working directory... so be careful. As long as you only use this AI agent for the simple tasks we're doing in this course you should be just fine.

! Assignment
"""
# Create a function in the functions directory 'run_python_file(working directory, file_path)
def run_python_file(working_directory, file_path):
    # If the file_path is outside the working directory, raise a string with an error
    working_dir_abs_path = os.path.abspath(working_directory)


    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        if not file_abs_path.startswith(working_dir_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_abs_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a python file.'
        result = subprocess.run(args=['python3', file_abs_path], capture_output=True, text=True, timeout=30)    
        stdout = f'"STDOUT:"\n{result.stdout}'
        stderr = f'"STDERR:"\n{result.stderr}\nProcess exited with code {result.returncode}'
        if result.returncode != 0:
            return stderr
        if len(result.stdout.strip()) < 1:
            return "No output produced"
        
        return stdout



    
    except Exception as e:
        return f'Error: executing Python file: {e}'
    



def main():
    result = run_python_file("calculator", "none.py")
    print(result)

if __name__ == "__main__":
    main()