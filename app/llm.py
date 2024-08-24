from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(".env")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Context for generating a new tool_info_module
context_generation = "You are a coding assistant that returns a working python tool_info_module file for a given CLI command, given other <CLI command,tool_info_module> pairs."

# Context for refining an existing tool_info_module based on test results
context_refinement = "You are a coding assistant that returns a refined python tool_info_module file for a given CLI command, given the result of a test_tool_info run."

def strip_python_completion(completion):
    # Remove Python code block markers from the completion text
    completion = completion.replace("```python","").replace("```","").strip()
    return completion

def generate_tool_info_module(prompt, context):
    # Generate a tool_info_module using the OpenAI API with the given prompt and context
    completion = client.chat.completions.create(
        #model="gpt-4o",
        #model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated tool_info_module from the completion response
    tool_info_module_raw = completion.choices[0].message.content
    tool_info_module = strip_python_completion(tool_info_module_raw)
    return tool_info_module

def build_refinement_prompt(module_test_result, tool_info_module):
    # Build a prompt for refining the tool_info_module based on the test result
    prompt = f"Benchexec's test_tool_info returned this result for the following tool-info module\n" \
            f"Result:\n{module_test_result}\n\ntool-info module tested:\n{tool_info_module}\n\nPlease fix/improve the tool-info module accordingly or try to reduce warnings\n" \
            "Return python code only."
    return prompt