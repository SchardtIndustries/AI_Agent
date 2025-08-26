import os
import google.generativeai
from google.genai import types
from google.generativeai import GenerativeModel
model = google.generativeai.GenerativeModel('gemini-pro')
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
def get_files_info(working_directory, directory="."):
    comb_dir = os.path.join(working_directory, directory)
    abs_wd = os.path.abspath(working_directory)
    abs_wk = os.path.abspath(comb_dir)
    if not abs_wk.startswith(abs_wd):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_wk):
        return(f'Error: "{directory}" is not a directory')

    names_list = os.listdir(abs_wk)
    output_lines = []

    for item_name in names_list:
        full_path = os.path.join(abs_wk, item_name)
        size = os.path.getsize(full_path)
        line = f"-{item_name}: file_size= {size} bytes, is_dir={os.path.isdir(full_path)}"
    
        output_lines.append(line
                        )
    final_output = "\n".join(output_lines)

    return(final_output)
