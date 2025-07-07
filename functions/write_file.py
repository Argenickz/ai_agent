import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs_path = os.path.abspath(working_directory)
    file_absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if file_absolute_path.startswith(working_dir_abs_path):
            dir_name = os.path.dirname(file_absolute_path)
            if not os.path.exists(dir_name):
                
                os.makedirs(dir_name)

            with open(file_absolute_path, "w") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into a file in the given directory, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory where the file to write to is, relative to the working directory."),
            "content": types.Schema(
                type=types.Type.STRING,
                description=" The content to be written into the file."
            )    
        }
    )
)

