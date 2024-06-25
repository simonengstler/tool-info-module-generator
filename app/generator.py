from dotenv import load_dotenv
import os
import app.command_input as input
import app.logging as logging
import app.llm as llm
import app.test_exec as test_exec

load_dotenv(".env")

refinement_iterations = int(os.environ.get("REFINEMENT_ITERATIONS"))

def create_tool_info_module_file(tool, cli_command, log_folder):
    
    # Iterate over all prefixes and generate a tool_info_module for each
    for prefix in os.listdir('template/prefixes'):
        if prefix.startswith("p0"):
            # skip p0 because of bad results
            continue
        if not prefix.endswith(".txt"):
            continue
        with open(f'template/prefixes/{prefix}', 'r') as f:
            prompt_prefix = f.read()

        p_folder = logging.create_px_folder(log_folder, prefix)

        prompt = f"{prompt_prefix}\n {cli_command}\n"

        tool_info_module = llm.generate_tool_info_module(prompt, llm.context_generation)

        module_test_result = None

        for iteration in range(1, refinement_iterations + 1):
            if iteration != 1:
                prompt = llm.build_refinement_prompt(module_test_result, tool_info_module)
                tool_info_module = llm.generate_tool_info_module(prompt, llm.context_refinement)

            tim_file_override = logging.save_tim_file(p_folder, tool_info_module, prompt, tool, iteration)

            module_test_result = test_exec.run_benchexec_test(p_folder, tim_file_override, tool)

            logging.save_results(p_folder, module_test_result, iteration)


def main():
    tool, cli_command = input.get_cli_command_from_file()
    # tool, cli_command = input.get_cli_command_from_user()

    log_folder = logging.create_unique_log_folder(tool)

    create_tool_info_module_file(tool, cli_command, log_folder)