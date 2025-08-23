import os

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
