import os

def write_file(working_directoroy, file_path, content):
    working_dir_abs_path = os.path.abspath(working_directoroy)
    file_absolute_path = os.path.abspath(os.path.join(working_directoroy, file_path))

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

def main():
    print(write_file("calculator", "pkg/morelorem.txt", "replace txt"))


if __name__=="__main__":
    main()

