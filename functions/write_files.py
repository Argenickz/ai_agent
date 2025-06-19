import os
"""
!Write Files
Up until now our program has been read-only. We'll give our agent the ability to write and overwrite files.
"""

# ! Create a new function. 'def write_file(working_directory, filepath, content):
def write_file(working_directory, file_path, content):
    # get a hold of the working directory absolute path
    working_directory_absolute_path = os.path.abspath(working_directory)

    # get a hold of the file_path working directory
    file_path_absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_path_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        # !If the file_path doesn't exist, create it. As always if there are any errors return a string representing the error, prefixed with 'Error:'.
        # Isolate the filepath
        new_filepath = os.path.dirname(file_path_absolute_path)

        # If the filepath doesn't exist create it
        if not os.path.exists(new_filepath):
            # Create the new directory(ies)
            os.makedirs(new_filepath)
            # Write to the file once the directory has ben created
            with open(file_path_absolute_path, "w") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            # Else just write to the directory that already exist
            with open(file_path_absolute_path, "w") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error processing file {file_path}\n{e}'
    

def main():
    result = write_file("calculator", "/temp/temp.txt", "this should not be allowed")
    print(result)
if __name__ == "__main__":
    main()