import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    """This functions list all the files in a directory, this directory needs the directory itself or needs to be inside the working directory"""
    # If the directory is outside the working argument is outside the working directory, return a string with an error.
    if directory:
        # Let's get a hold of the working directory's absolute path
        working_dir_absolute_path = os.path.abspath(working_directory)
        # print(f"working directory absolute path:\n{working_dir_absolute_path}\n")
        try:
            # Create the direcrory absolute path by joining the working directory absolute path and the directory
            directory_absolute_path = os.path.abspath(os.path.join(working_directory, directory))
            # print(f"directory absolute path:\n{directory_absolute_path}\n")

            # Check if the directory is inside the working directory
            if directory_absolute_path.startswith(working_dir_absolute_path):
                # check if it's an actual directory
                if os.path.isdir(directory_absolute_path):
                    result = []
                    items = os.listdir(directory_absolute_path)
                    for item in items:
                        entry = os.path.join(directory_absolute_path, item)
                        result.append(f"{item} file_size={os.path.getsize(entry)} is_dir={os.path.isdir(entry)}" )
                    return '\n'.join(result)
                if os.path.isfile(directory_absolute_path):
                    return f'Error: "{directory}" is not a directory'

            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        except Exception as e:
            return f'Error: {e}'
        
    return f'Error: Must provide a directory, directory cannot be {None}'
        
schema_get_files = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in the specified directory along with their size, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself."
            )
        }
    )
)




