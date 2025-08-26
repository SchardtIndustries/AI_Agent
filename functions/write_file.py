import os
import google.generativeai
from google.genai import types
from google.generativeai import GenerativeModel
model = google.generativeai.GenerativeModel('gemini-pro')

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write contents of file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of desired file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    # Convert absolute file_path to relative if needed
    if os.path.isabs(file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Combine paths
    combined_path = os.path.join(working_directory, file_path)
    abs_combined = os.path.abspath(combined_path)
    abs_wd = os.path.abspath(working_directory)
    
    # Security check
    if not abs_combined.startswith(abs_wd + os.sep):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    # Ensure the directory exists
    dir_name = os.path.dirname(abs_combined)
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
    except Exception as e:
        return f'Error: Failed to create directories - {str(e)}'
    
    # Write content, overwriting if file exists
    try:
        with open(abs_combined, 'w') as f:
            f.write(content)
    except Exception as e:
        return f'Error: Failed to write to file - {str(e)}'
    
    # Return success message
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'   
