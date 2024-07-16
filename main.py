from app.generator import generator
import argparse
from dotenv import load_dotenv, set_key

load_dotenv(".env")

def add_env_variable(key, value):
    # Save the environment variable to the .env file
    set_key(".env", key, str(value), quote_mode='never')
    print(f"Environment variable '{key}' set to '{value}' in .env file.")

def main():
    parser = argparse.ArgumentParser(description="Autogenerate tool-info modules for BenchExec using GPT-3.5.")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subcommands to set environment variables
    parser_set_openai_key = subparsers.add_parser('set_openai_key', help="Set the OpenAI API key")
    parser_set_openai_key.add_argument('openai_key', type=str, help="OpenAI API key to be added to the .env file")

    parser_set_execution_iterations = subparsers.add_parser('set_execution_iterations', help="Set the execution iterations")
    parser_set_execution_iterations.add_argument('execution_iterations', type=int, help="Execution iterations to be added to the .env file")

    parser_set_refinement_iterations = subparsers.add_parser('set_refinement_iterations', help="Set the refinement iterations")
    parser_set_refinement_iterations.add_argument('refinement_iterations', type=int, help="Refinement iterations to be added to the .env file")

    parser_set_python_lib_path = subparsers.add_parser('set_python_lib_path', help="Set the Python library path")
    parser_set_python_lib_path.add_argument('python_lib_path', type=str, help="Python library path to be added to the .env file")

    # Subcommand to run the tool info-module process
    parser_generator = subparsers.add_parser('generator', help="Run the tool-info module process")

    args = parser.parse_args()

    if args.command == "set_openai_key":
        add_env_variable("OPENAI_API_KEY", args.openai_key)
    elif args.command == "set_execution_iterations":
        add_env_variable("EXECUTION_ITERATIONS", args.execution_iterations)
    elif args.command == "set_refinement_iterations":
        add_env_variable("REFINEMENT_ITERATIONS", args.refinement_iterations)
    elif args.command == "set_python_lib_path":
        add_env_variable("PYTHON_LIB_PATH", args.python_lib_path)
    elif args.command == "generator":
        generator()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()