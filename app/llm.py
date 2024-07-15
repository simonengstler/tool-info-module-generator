from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(".env")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

context_generation = "You are a coding assistant that returns a working python tool_info_module file for a given CLI command, given other <CLI command,tool_info_module> pairs."
context_refinement = "You are a coding assistant that returns a refined python tool_info_module file for a given CLI command, given the result of a test_tool_info run."

def strip_python_completion(completion):
    completion = completion.replace("```python","").replace("```","").strip()
    return completion

def generate_tool_info_module(prompt, context):
    completion = client.chat.completions.create(
        #model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    tool_info_module_raw = completion.choices[0].message.content
    tool_info_module = strip_python_completion(tool_info_module_raw)
    return tool_info_module

def build_refinement_prompt(module_test_result, tool_info_module):
    prompt = f"Benchexec's test_tool_info returned this result for the following tool-info module\n" \
            f"Result:\n{module_test_result}\n\ntool-info module tested:\n{tool_info_module}\n\nPlease fix/improve the tool-info module accordingly or try to reduce warnings\n" \
            "Return python code only."
    return prompt