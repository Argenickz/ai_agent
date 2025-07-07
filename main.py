import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.functions_list import available_functions
from functions.call_functions import call_function

def main():
    
    load_dotenv()
    model = "gemini-2.0-flash-001"
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
   
        print(
            "Welcome to the CLI AI Agent\n" \
            "Use in the following format:\n" \
            "python3 main.py <'Your prompt here'>"
        )
        sys.exit(1)
    # =============================================
    system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function call as it is automatically injected for security reasons.

If the user asks for help fixing bugs in the code, as long as they are in within the confines of the working directory, you're allowed to make  use of the above provided operation to changes to files, test and fix codebases.

"""
    messages = [
        types.Content(
                role="user",
                parts=[types.Part(text=user_prompt)]
            )
        ]
    # =============================================

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # =============================================

    for x in range(20):
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                )
        )

        # =============================================
        verbose = "--verbose" in sys.argv
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if not response.function_calls:
            print(response.text)
            return response.text
        function_responses = []

        
        #!1.  For each iteration, check the '.candidates' property of the response. It's alist of response variations, and in particular it contains the equivalent of "I want to call (x function), so we need to add it to our conversation. Iterate over each '.candidate' and add its '.content' to the messages list."
        # I will to do the logic first on one iteration, then we add the loop
        # Check if a list of candidates exist in the response
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        
        for function_call_part in response.function_calls:
            # this is where the function gets called
            # !2. After each actual function call, append the returned 'types.Content' to the 'messages' as well. This is the equivalent of "Here's the result of (x function)" 
            function_call_result = call_function(function_call_part, verbose)
            messages.append(function_call_result)

            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
          
    print(response.text)
    if not function_responses:
        raise Exception("error, no function responses generated")
            

if __name__ == "__main__":
    main()



"""
! Agents
So we've got some function calling working but, it's not fair to call our program an 'agent' yet for one simple reason:
 
It has no feedback loop.

A key part of an "Agent", as defined by AI-influencer-hype-bros, is that it can continuously use its tools to iterate on its own results. So we're going to build two things:

1. A loop that will call the LLM over and over.

2. A list of messages in the "conversation". It will look something like this:
    . User: "Please fix the bug in the calculator"
    . Model: "I want to call get_files_info..."
    . Tool: "Here's the result of get_files_info..."
    . Model: "I want to call get_file_content..."
    . Tool: "Here's the result of get_file_content..."
    (etc...)

! Assignment

1. Create a loop that iterates at most 20 times(this will stop our agent from spinning its wheels forever).

    1. In each iteration check the '.candidates' property of the response. It's a list of response variations, and in particular it contains the equivalent of "I want to call get_files_info...", so we need to add it to our conversation. Iterate over each candidate and add its '.contents' to your messages list.

    2. After each actual function call, append the returned "types.Content" to the messages as well. This is the equivalent of "Here's the result of get_files_info"

    3. After each iteration, if a function was called, you should iterate again(unless max iterations was reached). Otherwise, you should print the LLM's final response(the '.text' property of the response) and break out- this means the agent is done with the task!(or failed miserably which happens as well)

    4. This might already be happening, but make sure that with each call to 'client.models.generate_content', you're passing in the entire message list so that the LLM always does the 'next step' based on the current state.

2. Test your code. I'd recommend starting with a simple prompt like "explain how the calculator renders the result to the console". This is what I got:
    - Calling function: get_files_info
    - Calling function: get_files_content
    - Calling function: get_files_info
    - Calling function: get_files_info

Final response:
Okay, I've examined the `render` function in `pkg/render.py`. Here's how it works:

1.  **Formats the result:** It first checks if the result is a float that can be represented as an integer. If so, it converts it to an integer string. Otherwise, it converts the result to a string.
2.  **Calculates box width:** It determines the width of the box that will surround the expression and result, based on the longer of the two strings.
3.  **Builds the box:** It creates a list of strings, each representing a line of the box. This includes the top and bottom borders, the expression, an equals sign, and the result, all padded with spaces to fit within the box.
4.  **Joins the lines:** Finally, it joins the lines of the box with newline characters to create a single string that can be printed to the console.

So, the calculator renders results to the console by formatting the expression and result into a box-like structure using ASCII characters. The `render` function takes the expression and result as input and returns the formatted string, which is then printed to the console in `main.py`.

` You may or may not need to make adjustments to your system prompt to get the LLM to behave the way you want. You're a prompt engineer now so act like one!.

"""
