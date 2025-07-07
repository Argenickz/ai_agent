import os
import subprocess
from google.genai import types

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
                        arguments.extend(args)
                    output = []
                    answer = subprocess.run(arguments, timeout=30, capture_output=True, text=True, cwd=working_dir_abs_path)
                    stdout = answer.stdout
                    stderr = answer.stderr
                    format = f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
                    if answer.returncode != 0:
                        return f"{format}\nProcess exited with code {answer.returncode}"
                    # Im only checking if there is an stdout, while the output might be stderr
                    if stdout:
                        output.append(stdout)
                    if stderr:
                        output.append(stderr)
                    
                    return '\n'.join(output) if output else "No output produced"
                    
                    
                return f'Error: "{file_path}" is not a Python file.'
            return f'Error: File "{file_path}" not found.'
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to run the python file from, relative to the working directory."
            )
        }
    )
)
