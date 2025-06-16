import os


"""
! Get Files
We need to give our agent te ability to do stuff. We'll start by giving it the ability to list the content of a directory and see the file's metadata (name and size).

Before we give the LLM the ability to this new 'get files' function, let's just build the function itself. Now remember, LLMs work with text, so our goal with this function will be for it to accept a directory path, and return a string that represent the contents of that directory.
"""

def get_files_info(working_directory, directory=None):
    # if the directory is not none proceed
    try:
        if directory != None:
            # Create an absolute path for the working directory
            working_directory_abssolute_path = os.path.abspath(working_directory)
            # Create an absolute path for the directory
            directory_absolute_path = os.path.abspath(os.path.join(working_directory, directory))
            
            # Check if the directory is inside the working directory
            if directory_absolute_path.startswith((working_directory_abssolute_path)):
                # Check if the directory is a valid path
                if os.path.isdir(directory_absolute_path):
                    # Todo this is where the logic for the items in the directory goes
                    items = os.listdir(directory_absolute_path)
                    report_list = []
                    for item in items:
                        entry = os.path.join(directory_absolute_path, item)
                        report_list.append(
                            f"- {item}: file_size={os.path.getsize(entry)} bytes, is_dir={os.path.isdir(entry)}"
                        )
                    report = '\n'.join(report_list)
                    return report
                elif os.path.isfile(directory_absolute_path):
                    return f'Error: "{directory}" is not a directory'
                # if the directory exists
                else:
                    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            else:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                
        
        if directory == None or not os.path.isdir(os.path.join(working_directory, directory)):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error processing files: {e}"

# Let's call the function with the working directory set as calculator, and the directory set at pkg inside the working directory

# def main():
#     test = get_files_info('calculator', 'pkg')
#     print(test)

# if __name__ == "__main__":
#     main()




"""
! Get File Content
Now that we have a function that can get contents of a directory, we need one that can get contents of a file. Again, we'll just return the file contents as a string, or perhaps an error string if something went wrong.
"""

# Create a new functions in your functions directory to get the contents of a file
def get_file_content(working_directory, filepath):
    try:
        print('processing...\n')
        # Create an absolute path for the working directory
        directory_absolute_path = os.path.abspath(working_directory)
        print(f"working directory absolute path:\n{directory_absolute_path}\n")

        # Create an absolute path for the filepath
        file_absolute_path = os.path.abspath(os.path.join(working_directory, filepath))
        print(f"file absolute path:\n{file_absolute_path}\n")

        # Check if the file is inside the working direcrtory
        if file_absolute_path.startswith(directory_absolute_path):
            print("this file is in the working directory")
            # check if the filepath is a valid file
            if os.path.isfile(file_absolute_path):
                print("this is where the logic for the item goes.")
                # Read the file and return its contents as a string.
                # If the file is longer than 1000 characters, truncate it to 1000 characters and append this message to the end:
                    # [...File "{file_path}" truncated at 1000 characters]
                # ! We don't want to accidentally read a gigantic file and send all that data to the LLM, that's a good way to burn through our token limit.

            else:
                return f'Error: File not found or is not a regular file: "{filepath}"'
        else:
            return f'Error: Cannot read "{filepath}" as it is outside the permitted working directory'
    except Exception as e:
        print(f"Error processing files: {e}")


# Filepaths test to run:
#   main.py, pkg/calculator.py, /bin/cat





def main():
    result = get_file_content("calculator", 'main.py')
    print(result)

if __name__ == "__main__":
    main()