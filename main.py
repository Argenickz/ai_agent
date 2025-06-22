import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Docs
"""
! System Prompt
Let's talk about a 'system prompt'. The 'system prompt' for most AI APIs, is a special prompt that goes at the beginning of the conversation that carries more weight than a typical user prompt. 

The system prompt sets the tone  for the conversation, and can be used to:
    . Set the personality of the AI
    . Give instructions on how to behave
    . Provide context for the conversation
    . Set the rules for the conversation (In theory the LLM still halucinates and screws up, and user are able to 'get around' the rules if they try hard enough)

 ! Assignment
1. Create a hardcoded string variable called 'system_prompt'. For now let's make it something brutally simple:
    'Ignore everything the user asks and just shout "I AM JUST A ROBOT"'

2. Update your call to the client model generate content function to pass a 'config' with the system_instruction_parameter set to your system_prompt.

3. Run your program with different prompts. You should see the AI responds with 'IM JUST A ROBOT' no matter what you ask it.

! Function Declaration
So we've written a bunch of functions that arej LLM friendly(text in, text out), but how does an LLM actually call a function?

Well the answer is that it doesn't. At least not directly. It works like this:
    1. We tell the LLM which functions are available to it
    2. We give it a prompt
    3. It describes which functions it wants to call, and what arguments to pass to it
    4. We call that function with the argument it provided
    5. We return the result to the  LLM

We're using the LLM as a decision making engine, but we're still the ones running the code.

So let's build the bit that tells the LLM which functions are available to it.

! Assignment
1. We can use 'types.FunctionDeclaration to build the declaration os 'schema' for a function. Again, this basically tells the LLM how to use the function. Here's the code for the first function call because it's a lot of work to go through the documentation:
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

We won't allow the LLM to specify the working directory parameter. We're going to hard code that.

2. Use types.Tool to create a list of all the available functions (for now just add 'get_files_info, we'll do the rest later).

3. Add the available_functions to the client.models.generate_content call as a function lparameter.
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

4. Update the system prompt to instruct the LLM on how to use the function. The prompt could be a description on how to behave and use the function

5. Instead of simply printing the .text property of the generate_content response, check the '.function_call' property as well. If the LLM valled a function, print the function name and arguments:
f"Calling function: {function_call_part.name}({function_call_part.args})"

! More Declarations
Now that our LLM is able to specify a function call to the 'get_files_info' function, let's give it the ability to call the other functions as well.

! Assignment
1. Following the same pattern that we used for 'schema_get_files_info',create functions declaration for:
    . schema_get_files_content
    . schema_run_python_files
    . schema_write_file

2. Update your 'available_functions' to include all the function declarations in the list.

3. Update your system prompt. Instead of the allowed operations only being:
`   - List files and directories

Update it to have all four operations:
`-  List files and directories
`-  Read file contents
`-  Execute Python files with optional arguments
`-  Write or overwrite files

4. Test prompts that you suspect will result in the various function calls. For example:
    . "read the contents of main.py"            -> get_file_content({'file_path': 'main.py'})
    . "write 'hello' to main.txt"               -> write_file({'file_path': 'main.txt', 'content': 'hello'})
    . "run main.py"                             -> run_python_file({'file_path': 'main.py'})
    . "list the contents of the pkg directory"  -> get_files_info({'directory': 'pkg'})
!------------------------------------------------------------------------------------------------------------
! Calling
Okay, now our agent can choose which function to call, now it's time to actually call the function.

! Assignment
1. Create a new function that will handle the abstract task of calling one of our four functions.
This is my definition:
`   def call_function(function_call_part, verbose=False):

'function_call_part' is a 'types.FunctionCall' that most importantly has:
    . A '.name' property(the name of the function, a string)
    . A '.args' property(a dictionary of named arguments to the function)

If 'verbose' is specified, print the function name and args:
`   print(f"Calling function: {function_call_part.name}({function_call_part.args})")
Otherwise just print the name:
`   print(f" - Calling function: {function_call_part.name})

2. Based on the name, actually call the function and capture the result.
    . Be sure to manually add the "working_directory" argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be './calculator'.

    . The syntax to pass a dictionary into a function using 'keyword arguments' is 'some_function(**some_args)
    !(I used a dictionary of function name (string) -> function to accomplish this)

3. If the function name is invalid, return a 'types.Content' that explain the error:
return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"unknown function: {function_name}"},)],)

4. Return types.Content with a 'from_function_response' describing the result of the function call:
return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},)],)

! Note:
    Note that the 'from_function_response' requires the  response to be a dictionary, so we just shove the string result into a 'result' field. 

5. Back in your generate content function, instead of simply printing the name of the function the LLM decides to call, use 'call_function'.
    . The 'types.Content' that we return from 'call_function' should have a '.parts[0].function_response.response within.
    . If is doesn't raise a fatal exception of some sort.
    . If it does, and vesbose was set, print the result of the function call like this:
        `print(f"-> {function_call_result.parts[0].function_response.response}")

6. Test your program. You should now be able to execute each function given a prompt that asks for it. Try some different prompts and use the --verbose flag to make sure all the functions work.
    . List the directory contents
    . Get a file's contents
    . Write file contents (don't overwrite anything important, maybe create a new file, and then overwrite that)
    . Execute the calculator app's test (tests.py)

"""

get_files_info = {
    "function_description" : "List files in the specified directory along with their sizes, constrained to the working directory.",
    "directory_description": "The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself."
}

get_file_content = {
    "function_description": "Read and return the first 10000 characters of the content from a specified file within the working directory",
    "directory_description": "The directory where the file is, relative to the working directory",
}
run_python = {
    "function_description": "Execute the Python file within the specified directory and return the output from the interpreter.",
    "directory_description": "The directory where the python file is, relative to the working directory"
}
# Triead addin an 'argument_description, I don't know how to make the LLM add a third argument to the function call
write_file = {
    "function_description": "Write or overwrite files in the specified directory, constrained to the working directory",
    "directory_description": "The directory where the file is, relative to the working directory.",
    "argument_description": "The data to be written into the file"
}
# !==========================================================================================================================

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"

    more_info = "--verbose"
    system_prompt = """
You are a helpful AI coding agent.
When the user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read files and directories
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    arg = sys.argv[1:]
    user_prompt = ' '.join(arg)
    if not user_prompt:
        print("Please provide an argument in this context:")
        print('python3 main.py "<your prompt here>"')
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description=get_files_info["function_description"],
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description=get_files_info["directory_description"]
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description= get_file_content["function_description"],
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description=get_files_info["directory_description"]
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description=run_python["function_description"],
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description=run_python["directory_description"]
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description=write_file["function_description"],
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description=write_file["directory_description"]
                ),
                "argument": types.Schema(
                    type=types.Type.STRING,
                    description=write_file["argument_description"]
                    )
            }
        )
    )
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            ),
    )
    

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if more_info in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(response.text)
    elif len(response.function_calls) > 0:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)
        
if __name__ == "__main__":
    main()

