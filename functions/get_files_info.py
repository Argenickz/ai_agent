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



