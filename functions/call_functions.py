"""
! Calling
Our agent can choose which functions to call, now it's time to actually call the functions.

! Assignment
1. Create a new function that will handle the abstract task of calling one of our four functions. This is the definition:
` def call_function(function_call_part, verbose=False):

'function_call_part' is a 'types.FunctionCall' that most importantly has:
    . A '.name' property (the name of the function, a string)
    . A '.args' property ( a dictionary of named arguments to the function)

If verbose is specified, print the function name and args:
` print(f"Calling function: {function_call_part.name}({function_call_part.args}))

Otherwise, just print the name:
` print(f" -Calling function: {function_call_part.name}")

2. ...
# todo might have to use a seer stone on this one, I really don't get it...Used a seer stone, but try to solve it anyways with the clues below and the clues in main.py


"""
WORKING_DIRECTORY = "./calculator"
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

from google.genai import types

# Create a function that will handle the task of calling one of our functions
def call_function(function_call_part, verbose=False):
    # If verbose if specified, print the function name and args
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        # Otherwise, just print the function name.
    else:   
        print(f"Calling function: {function_call_part.name}")
    
    # Create a dictionary with the function names as a key and the functions themselves as values
    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    # Get a hold of the function name
    function_name = function_call_part.name

    # If the function name is not a valid function return a types.Content that explain the error.
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )
    # Based on the name, actually call the function and capture the result.
    args = dict(function_call_part.args)
    # Be sure to add the 'working_directory' argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be './calculator'
    args["working_directory"]=WORKING_DIRECTORY

    function_call_result = functions[function_name](**args)

    # Return 'types.Content' with a 'from_function_response' describing the result of the function call.
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_call_result}
            )
        ]
    )

    