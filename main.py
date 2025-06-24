import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    
    load_dotenv()
    model = "gemini-2.0-flash-001"
    user_prompt = sys.argv[1]
    # =============================================
    if not user_prompt:
        print(
            "Welcome to the CLI AI Agent\n" \
            "Use in the following format:\n" \
            "python3 main.py <'Your prompt here'>"
        )
        sys.exit(1)
    # =============================================

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
    response = client.models.generate_content(
        model=model,
        contents=messages
    )
    # =============================================
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()

# Todo/ Started over with a new branch 'anew' to create the project from 'almost zero' cause I was all over the place, I need to create directories for every new function, also I need to group functions that go together.

