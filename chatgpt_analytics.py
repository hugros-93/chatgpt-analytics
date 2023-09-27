import json
import openai
import re
import os

openai.api_key_path = 'API_KEY.txt'

def ask_chat_gpt():

    # Load prompt
    with open("prompt/context.txt", "r") as f:
        prompt_text = f.read()

    # Input
    input_text = input('Input:\n')
    with open("input_prompt/input_prompt.txt", "w") as f:
        f.write(input_text)

    # Generate
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": input_text}
        ]
    )

    # Output
    with open(f'output_chatgpt/output_chatgpt.json', 'w') as f:
        json.dump(response, f)

    return response

def plot_from_response(response):

    # Extract python code from response
    response = response["choices"][0]["message"]["content"]
    pattern = r'```python(.*?)```'
    code_blocks = re.findall(pattern, response, re.DOTALL)
    code_output = "\n".join([x.strip() for x in code_blocks])

    # Clean export folder
    dir = 'output_charts/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Exec code
    exec(code_output)

if __name__ == "__main__":
    response = ask_chat_gpt()
    plot_from_response(response)