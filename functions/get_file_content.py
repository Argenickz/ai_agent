import os
MAX_CHARACTERS = 10000

def get_file_content(working_directory, file_path):
    """This function reads a file in an specified directory and returns the first 10000 characters"""
    try: 
        working_dir_absolute_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if absolute_file_path.startswith(working_dir_absolute_path):
            if os.path.isfile(absolute_file_path):
                with open(absolute_file_path, 'r') as file:
                    content = file.read()
                    if len(content) > MAX_CHARACTERS:
                        return f'{content[:MAX_CHARACTERS]}\n[...File "{file_path}" truncated at 10000 characters]'
                    return content
            return f'Error: File not found or is not a regular file: "{file_path}"'
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working direcrtory'
    except Exception as e:
        return f'Error: {e}'

def main():
    result = get_file_content("calculator", "main.py")
    print(result)

if __name__=="__main__":
    main()


