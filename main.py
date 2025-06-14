import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Set all this inside a main function
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"

    more_info = "--verbose"

    user_prompt = sys.argv[1]
    if not user_prompt:
        print("Please provide an argument in this context:")
        print('python3 main.py "<your prompt here>"')
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(model=model, contents=messages)

   

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if more_info in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    main()