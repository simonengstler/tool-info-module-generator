import subprocess

def run_benchexec_test(p_folder, tool):
    # Construct the command to set PYTHONPATH and run the benchexec test_tool_info command
    command = f"export PYTHONPATH={p_folder}:$PYTHONPATH && python3 -m benchexec.test_tool_info --no-container .{tool} --tool-directory template/mock_exes/"

    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, capture_output=True)
        return result.stderr.decode()
    except subprocess.CalledProcessError as e:
        # Return the error message if the command failed
        return e.stderr.decode()