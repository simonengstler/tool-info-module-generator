import os
import datetime

def create_unique_log_folder(tool):
    # Create a unique log folder based on the current timestamp and tool name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = os.path.join("logs", f"{tool}_{timestamp}")
    os.makedirs(log_folder, exist_ok=True)
    return log_folder

def create_px_folder(log_folder, prefix):
    # Create a subfolder within the log folder for the given prefix
    p_folder = os.path.join(f"{log_folder}", f"{prefix.replace('.txt','')}")
    os.makedirs(p_folder, exist_ok=True)
    return p_folder

def save_tim_file(p_folder, tool_info_module, prompt, tool, iteration):
    # Save the prompt to a file in the prefix folder
    prompt_file = os.path.join(p_folder, f"prompt_it{iteration}.txt")
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    # Save the tool info module to a file with the iteration number in the prefix folder
    tim_file_it = os.path.join(p_folder, f"{tool}_it{iteration}.py") 
    with open(tim_file_it, 'w') as f:
        f.write(tool_info_module)

    # Save the tool info module to a file that overrides the previous version in the prefix folder
    tim_file_override = os.path.join(p_folder, f"{tool}.py") 
    with open(tim_file_override, 'w') as f:
        f.write(tool_info_module)

    return tim_file_override

def save_results(p_folder, module_test_result, iteration):
    # Save the test results to a file in the prefix folder
    result_file = os.path.join(p_folder, f"benchexec_result_it{iteration}.txt")
    with open(result_file, 'w') as f:
        f.write(module_test_result)

def save_best_result_if_available(best_result, tool):
    # Save the best result to a file in the results folder with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if not best_result:
        print("No valid result could be generated.")
    else:
        os.makedirs("results", exist_ok=True)

        # Save the best result to a file in the results folder
        best_result_log = os.path.join("results", f"{tool}_{timestamp}.txt")
        best_result_tim = os.path.join("results", f"{tool}_{timestamp}.py")

        with open(best_result_tim, 'w') as f:
            f.write(best_result[0])

        with open(best_result_log, 'w') as f:
            f.write(best_result[1])

        print("Check 'results' for the generated tool-info module. Other results can be found in the log folder.")
        