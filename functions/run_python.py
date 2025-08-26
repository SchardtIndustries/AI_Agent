import os
import subprocess
import google.generativeai
from google.genai import types
from google.generativeai import GenerativeModel
model = google.generativeai.GenerativeModel('gemini-pro')

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of desired file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="arguments to pass to the file",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    # Reject absolute paths
    if os.path.isabs(file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Combine paths and get absolute path
    combined_path = os.path.join(working_directory, file_path)
    abs_combined = os.path.abspath(combined_path)
    abs_wd = os.path.abspath(working_directory)
    
    # Ensure the file is inside working_directory
    if not abs_combined.startswith(abs_wd + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file exists
    if not os.path.exists(abs_combined):
        return f'Error: File "{file_path}" not found.'
    
    # Check if it's a Python file
    if not abs_combined.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    # Prepare to execute
    command = ['python', abs_combined] + args
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )
        # Prepare output
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr.strip()}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        if not output_parts:
            return "No output produced."
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
