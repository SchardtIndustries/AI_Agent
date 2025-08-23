import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)


def main():

    print("Hello from ai-agent!")
    
    verbose = False
    if '--verbose' in sys.argv:
        verbose = True
        sys.argv.remove('--verbose')

    if len(sys.argv) < 2:
        print("Error: No argument provided")
        sys.exit(1)
    arg_value = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=arg_value)]),
            ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )
    
    
    if verbose:
        print(f"User prompt: {arg_value}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == "__main__":
    main()
