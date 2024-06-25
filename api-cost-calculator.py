import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(".env")

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Function to generate a response from the OpenAI API and calculate the cost
def generate_response(prompt):
    completion = client.chat.completions.create(
        #model="gpt-4-turbo",
        #model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    usage = completion.usage

    # Extract token usage using dot notation
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    # Calculate cost (assuming $0.002 per 1,000 tokens)
    cost_per_1000_tokens = 0.002 # $0.0005 input + $0.0015 output
    cost = (total_tokens / 1000) * cost_per_1000_tokens

    return response, prompt_tokens, completion_tokens, total_tokens, cost

# Main function
def main():

    # gpt-3.5-turbo
    # Joke: $0.000074
    # P0: $0.001620
    # P2: $0.003408
    
    # gpt-4o
    # Joke: $0.000074
    # P0: $0.000690
    # P2: $0.004344

    #prompt = "Tell me a joke about programming."
    
    with open(f'template/prefixes/p0.txt', 'r') as f:
        prompt = f.read()

    response, prompt_tokens, completion_tokens, total_tokens, cost = generate_response(prompt)
    print(f"Response:\n{response}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Completion Tokens: {completion_tokens}")
    print(f"Total Tokens: {total_tokens}")
    print(f"Cost: ${cost:.6f}")

if __name__ == "__main__":
    main()
