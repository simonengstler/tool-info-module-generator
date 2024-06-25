import subprocess

def run_benchexec_test(p_folder, tim_file, tool):
    # copy the tool_info_module to the benchexec python library
    command = f"sudo cp {tim_file} /usr/lib/python3/dist-packages/benchexec/tools"
    subprocess.run(command, shell=True)

    command = f"python3 -m benchexec.test_tool_info {tool} --no-container"
    return subprocess.run(command, shell=True, cwd=p_folder, capture_output=True, text=True)