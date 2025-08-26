import os
from config import MAX_CHARS
import google.generativeai
from google.genai import types
from google.generativeai import GenerativeModel
model = google.generativeai.GenerativeModel('gemini-pro')

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists contents of file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of desired file",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        # Join and resolve absolute paths
        combined_path = os.path.join(working_directory, file_path)
        abs_file_path = os.path.abspath(combined_path)
        abs_working_directory = os.path.abspath(working_directory)

        # Check if the file is outside the working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Determine file size before reading
        file_size = os.path.getsize(abs_file_path)
        max_chars = MAX_CHARS

        # Read only up to MAX_CHARS characters
        with open(abs_file_path, 'r') as f:
            content = f.read(max_chars)

        # If the file is larger than MAX_CHARS, add truncation note
        if file_size > max_chars:
            return f'{content} [...File "{file_path}" truncated at {max_chars} characters]'
        else:
            return content
    except Exception as e:
        return f"Error: {str(e)}"
