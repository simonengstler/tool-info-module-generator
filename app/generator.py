from dotenv import load_dotenv
import os
import app.command_input as input
import app.logging as logging
import app.llm as llm
import app.test_exec as test_exec

load_dotenv(".env")

def create_tool_info_module_file(tool, cli_command):
    # Get the number of execution and refinement iterations from environment variables
    execution_iterations = int(os.environ.get("EXECUTION_ITERATIONS"))
    refinement_iterations = int(os.environ.get("REFINEMENT_ITERATIONS"))

    results = []
    for _ in range(execution_iterations):
        # Create a unique log folder for the current tool
        log_folder = logging.create_unique_log_folder(tool)

        # Iterate over all prefix files in the 'template/prefixes' directory
        for prefix in os.listdir('template/prefixes'):
            if not prefix.endswith(".txt"):
                continue
            # Skip prefixes that start with 'p0' or 'p3' due to bad results
            if prefix.startswith("p0") or prefix.startswith("p3"):
                continue
            with open(f'template/prefixes/{prefix}', 'r') as f:
                prompt_prefix = f.read()

            # Create a folder for the current prefix
            p_folder = logging.create_px_folder(log_folder, prefix)

            # Construct the initial prompt
            prompt = f"{prompt_prefix}\n {cli_command}\n"

            # Generate the initial tool info module using the prompt
            tool_info_module = llm.generate_tool_info_module(prompt, llm.context_generation)

            module_test_result = None

            # Refine the tool info module over multiple iterations
            for iteration in range(1, refinement_iterations + 1):
                if iteration != 1:
                    # Build a refinement prompt based on the previous test result
                    prompt = llm.build_refinement_prompt(module_test_result, tool_info_module)
                    # Generate a refined tool info module using the new prompt
                    tool_info_module = llm.generate_tool_info_module(prompt, llm.context_refinement)

                # Save the current tool info module and prompt to a file
                tim_file_override = logging.save_tim_file(p_folder, tool_info_module, prompt, tool, iteration)

                # Run the test on the current tool info module
                module_test_result = test_exec.run_benchexec_test(p_folder, tim_file_override, tool)
                results.append((tool_info_module, module_test_result))

                # Save the test results
                logging.save_results(p_folder, module_test_result, iteration)

    return results

def determine_and_log_best_result_if_available(results, tool):
    # Filter out invalid results that do not contain the required string
    results = list(filter(lambda x: "Command line SV-Benchmarks task:" in x[1], results))

    if not results:
        print("No valid result could be generated.")
        return

    # Determine the result with the least number of warnings
    best_result = min(results, key=lambda x: x[1].count("WARNING"))

    # Save the best result to a file
    logging.save_best_result_if_available(best_result, tool)

def generator():
    # Get the tool and CLI command from a file
    tool, cli_command = input.get_cli_command_from_file()
    # Alternatively, get the tool and CLI command from user input
    # tool, cli_command = input.get_cli_command_from_user()

    results = create_tool_info_module_file(tool, cli_command)

    determine_and_log_best_result_if_available(results, tool)