import os
import datetime

def create_unique_log_folder(tool):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = os.path.join("logs", f"{tool}_{timestamp}")
    os.makedirs(log_folder, exist_ok=True)
    return log_folder

def create_px_folder(log_folder, prefix):
    p_folder = os.path.join(f"{log_folder}", f"{prefix.replace('.txt','')}")
    os.makedirs(p_folder, exist_ok=True)
    return p_folder

def save_tim_file(p_folder, tool_info_module, prompt, tool, iteration):
    prompt_file = os.path.join(p_folder, f"prompt_it{iteration}.txt")
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    tim_file_it = os.path.join(p_folder, f"{tool}_it{iteration}.py") 
    with open(tim_file_it, 'w') as f:
        f.write(tool_info_module)

    tim_file_override = os.path.join(p_folder, f"{tool}.py") 
    with open(tim_file_override, 'w') as f:
        f.write(tool_info_module)

    return tim_file_override

def save_results(p_folder, module_test_result, iteration):
    result_file = os.path.join(p_folder, f"benchexec_result_it{iteration}.txt")
    with open(result_file, 'w') as f:
        f.write("stdout:\n")
        f.write(module_test_result.stdout)
        f.write("\n")
        f.write("stderr:\n")
        f.write(module_test_result.stderr)

