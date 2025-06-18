import os
"""
!Write Files
Up until now our program has been read-only. We'll give our agent the ability to write and overwrite files.
"""

# ! Create a new function. 'def write_file(working_directory, filepath, content):
def write_file(working_directory, file_path, content):
    # get a hold of the working directory absolute path
    working_directory_absolute_path = os.path.abspath(working_directory)
    print(f"this is the working difectory absolute path:\n{working_directory_absolute_path}\n")

    # get a hold of the file_path working directory
    file_path_absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    print(f"this is the file_path absolute path:\n{file_path_absolute_path}\n")

    if not file_path_absolute_path.startswith(working_directory_absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        # !If the file_path doesn't exist, create it. As always if there are any errors return a string representing the error, prefixed with 'Error:'.
        # If the file_path doesn't exist create it
        if not os.path.exists(file_path_absolute_path):
            print('the filepath doesnt exist create it\n')
            filename = os.path.basename(file_path_absolute_path)
            print(f"this is the filename: {filename}")
            # todo. Using dirname and os.path.base name I can get the directory name and the file name separately, even if they don't exist. if the filepath (using dirname) doesn't exits, create it. then with open(filename 'w') to write/rewrite to the file in said directory.


    except Exception as e:
        return f'Error processing file {file_path}\n{e}'
    

    
        




def main():
    result = write_file("calculator", "pkg/more_shit.txt", "hey I just met you, and this is craaazy!")
    print(result)
if __name__ == "__main__":
    main()