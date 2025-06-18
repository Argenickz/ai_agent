import os
"""
! Get File Content
Now that we have a function that can get contents of a directory, we need one that can get contents of a file. Again, we'll just return the file contents as a string, or perhaps an error string if something went wrong.
"""

# Create a new functions in your functions directory to get the contents of a file
def get_file_content(working_directory, filepath):
    try:
        # Create an absolute path for the working directory
        directory_absolute_path = os.path.abspath(working_directory)

        # Create an absolute path for the filepath
        file_absolute_path = os.path.abspath(os.path.join(working_directory, filepath))

        # Check if the file is inside the working direcrtory
        if file_absolute_path.startswith(directory_absolute_path):
            # check if the filepath is a valid file
            if os.path.isfile(file_absolute_path):
                with open(file_absolute_path, "r") as file:
                    text = file.read()
                    max_chars = 10000
                    if len(text) > max_chars:
                        return f'{text[0:max_chars]}\n[...File "{filepath}" truncated at 10000 characters]'
                    else:
                        return text
                # Read the file and return its contents as a string.
                # If the file is longer than 1000 characters, truncate it to 1000 characters and append this message to the end:
                    # [...File "{file_path}" truncated at 1000 characters]
                # ! We don't want to accidentally read a gigantic file and send all that data to the LLM, that's a good way to burn through our token limit.

            else:
                return f'Error: File not found or is not a regular file: "{filepath}"'
        else:
            return f'Error: Cannot read "{filepath}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error processing files: {e}"


# Filepaths test to run:
#   main.py, pkg/calculator.py, /bin/cat





def main():
    result = get_file_content("calculator", 'main.py')
    print(result)

if __name__ == "__main__":
    main()

# Todo Failed the CLI test, check and try again later...




