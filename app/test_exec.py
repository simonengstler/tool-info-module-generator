import subprocess
import os
from dotenv import load_dotenv

load_dotenv(".env")

def run_benchexec_test(p_folder, tim_file, tool):
    path_to_lib = os.environ.get("PYTHON_LIB_PATH")

    # Determine the shell and set the source command accordingly
    shell = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell:
        source_cmd = "source ~/.zshrc && echo $PATH"
    else:
        source_cmd = "source ~/.bashrc && echo $PATH"
    
    result = subprocess.run(source_cmd, shell=True, capture_output=True, text=True, executable=shell)
    
    # Extract the PATH from the sourced environment
    new_path = result.stdout.strip()
    
    # Set the new PATH to the environment
    os.environ["PATH"] = new_path

    # Copy the tool_info_module to the benchexec python library
    command = f"sudo cp {tim_file} {path_to_lib}/benchexec/tools"
    subprocess.run(command, shell=True)

    command = f"python3 -m benchexec.test_tool_info {tool} --no-container"
    return subprocess.run(command, shell=True, cwd=p_folder, capture_output=True, text=True).stderr
