from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess

load_dotenv(".env")

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

def generate_tool_info_module(prompt):

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a coding assistant that returns a fitting python tool_info_module file for a given CLI command, given other <CLI command - tool_info_module> pairs."},
        {"role": "user", "content": prompt}
  ]
    )
    print(completion)
    return completion.choices[0].message.content

# Define function to run benchexec with generated tool-info-module
def run_benchexec(tool_info_module_path):
    # Assuming benchexec command and options
    benchexec_command = ['benchexec', '--tool-info', tool_info_module_path, 'benchmark.xml']
    try:
        subprocess.run(benchexec_command, check=True)
        return True, None  # Successful execution
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')  # Failed execution, return error message

# Main function
def main():

    with open('prompt_prefix.txt', 'r') as f:
        prompt_prefix = f.read()

    #cli_command = input("Enter CLI command: ")
    cli_command = "cbmc --xml-ui task.c"

    prompt = f"{prompt_prefix}\n {cli_command}\n"
    print(f"Prompt:\n{prompt}")

    num_iterations = 1
    
    for i in range(num_iterations):

        tool_info_module = generate_tool_info_module(prompt)

        tool_info_module_path = f"tool_info_module.py"
        with open(tool_info_module_path, 'w') as f:
            f.write(str(tool_info_module))

        success = True
        error_message = None
        #success, error_message = run_benchexec(tool_info_module_path)

        # Check if execution was successful
        if success:
            print("Task successful!")
            break
        else:
            print(f"Iteration {i+1} failed with error:\n{error_message}")

            prompt = error_message
            # Provide error message to GPT-3.5 to generate a new tool-info-module
            # (This part needs integration with GPT-3.5 API)

if __name__ == "__main__":
    main()
