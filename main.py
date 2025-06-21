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
"""

get_files_info = {
    "function_description" : "List files in the specified directory along with their sizes, constrained to the working directory.",
    "directory_description": "The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself."
}

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

    schema_get_files_info= types.FunctionDeclaration(
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
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
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

