from dotenv import load_dotenv
import os
import app.command_input as input
import app.logging as logging
import app.llm as llm
import app.test_exec as test_exec

load_dotenv(".env")

def create_tool_info_module_file(tool, cli_command):
    execution_iterations = int(os.environ.get("EXECUTION_ITERATIONS"))
    refinement_iterations = int(os.environ.get("REFINEMENT_ITERATIONS"))

    results = []
    for _ in range(1, execution_iterations + 1):
        log_folder = logging.create_unique_log_folder(tool)

        # Iterate over all prefixes and generate a tool_info_module for each
        for prefix in os.listdir('template/prefixes'):
            if not prefix.endswith(".txt"):
                continue
            # deactivate p0 and p3 because of bad results
            if prefix.startswith("p0") or prefix.startswith("p3"):
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
                results.append((tool_info_module, module_test_result))

                logging.save_results(p_folder, module_test_result, iteration)

    return results

def determine_and_log_best_result_if_available(results, tool):
    # filter out all results that do not contain "Command line SV-Benchmarks task:" as they are not valid
    results = list(filter(lambda x: "Command line SV-Benchmarks task:" in x[1], results))

    if not results:
        print("No valid result could be generated.")
        return

    # determine the pair in results with the least occurrences of warnings
    best_result = min(results, key=lambda x: x[1].count("WARNING"))

    # save the best result to a file
    logging.save_best_result_if_available(best_result, tool)

def generator():
    # tool, cli_command = input.get_cli_command_from_file()
    tool, cli_command = input.get_cli_command_from_user()

    results = create_tool_info_module_file(tool, cli_command)

    determine_and_log_best_result_if_available(results, tool)