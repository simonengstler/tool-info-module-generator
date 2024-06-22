from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime
import subprocess

load_dotenv(".env")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_tool_info_module(prompt):
    #return "test"
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a coding assistant that returns a fitting python tool_info_module file for a given CLI command, given other <CLI command - tool_info_module> pairs."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def run_benchexec_test(p_folder, tool_info_module_file):
    # copy the tool_info_module_file to the directory
    command = f"sudo cp {tool_info_module_file} /usr/lib/python3/dist-packages/benchexec/tools"
    subprocess.run(command, shell=True)

    command = f"PATH=$PWD:$PATH python3 -m benchexec.test_tool_info {tool_info_module_file} --tool-directory ./template/mock_exes --no-container"
    return subprocess.run(command, shell=True, cwd=p_folder, capture_output=True, text=True)
    print("Command output:", result.stdout)
    print("Command error (if any):", result.stderr)

def main():

    #tool = "cbmc_1"
    #tool = "goblint_1"
    tool = "javac_1"

    with open(f'template/cmd/{tool}.txt', 'r') as f:
        cli_command = f.read()

    # Create a unique log folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = os.path.join("logs", f"{tool}_{timestamp}")
    os.makedirs(log_folder, exist_ok=True)


    for prefix in os.listdir('template/prefixes'):
        if not prefix.endswith(".txt"):
            continue
        with open(f'template/prefixes/{prefix}', 'r') as f:
            prompt_prefix = f.read()

        prompt = f"{prompt_prefix}\n {cli_command}\n"

        tool_info_module = generate_tool_info_module(prompt)
        cleaned_tool_info_module = tool_info_module.replace("```python","").replace("```","").strip()

        # Create a folder for the current p-file and save the generated tool_info_module as well as the prompt
        p_folder = os.path.join(f"{log_folder}", f"{prefix.replace('.txt','')}")
        os.makedirs(p_folder, exist_ok=True)
        tim_file = os.path.join(p_folder, f"{tool}.py") 
        with open(tim_file, 'w') as f:
            f.write(cleaned_tool_info_module)
        prompt_file = os.path.join(p_folder, "prompt.txt")
        with open(prompt_file, 'w') as f:
            f.write(prompt)

        # Run benchexec test on the generated tool_info_module
        result = run_benchexec_test(p_folder, tim_file)
        exex_result_file = os.path.join(p_folder, "benchexec_result.txt")
        with open(exex_result_file, 'w') as f:
            f.write(str(result))


if __name__ == "__main__":
    main()
