import json
import openai
import re
import os

openai.api_key_path = 'API_KEY.txt'

def ask_chat_gpt(input_text):

    # Load prompt
    with open("prompt_context.txt", "r") as f:
        prompt_text = f.read()

    # Load history
    try:
        with open("output_chatgpt/output_chatgpt_history.json", "r") as f:
            output_chatgpt_history = json.load(f)
    except:
        output_chatgpt_history = []
        print('No history!')

    # Generate
    messages=[
        {"role": "system", "content": prompt_text}
    ]
    messages = messages + output_chatgpt_history
    messages.append({"role": "user", "content": input_text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages
    )

    output_chatgpt_history.append({"role": "user", "content": input_text})

    # Load and update input prompt
    input_text = '- _' + input_text + '_'
    try:
        with open("input_prompt/input_prompt.txt", "r") as f:
            updated_input_text = f.read()
        updated_input_text = updated_input_text + '\n' + input_text
    except:
        updated_input_text = input_text
    with open("input_prompt/input_prompt.txt", "w") as f:
        f.write(updated_input_text)

    # Output chatgpt
    with open(f'output_chatgpt/output_chatgpt.json', 'w') as f:
        json.dump(response, f)

    # Update history
    with open(f'output_chatgpt/output_chatgpt_history.json', 'w') as f:
        json.dump(output_chatgpt_history, f)

    return response

def plot_from_response(response):

    # Extract python code from response
    response = response["choices"][0]["message"]["content"]
    pattern = r'```python(.*?)```'
    code_blocks = re.findall(pattern, response, re.DOTALL)
    code_output = "\n".join([x.strip() for x in code_blocks])

    # Clean export folder
    dir = 'output_charts/'
    chart_files = [x for x in os.listdir(dir) if x != '.gitignore']
    for f in chart_files:
        os.remove(os.path.join(dir, f))

    # Exec code
    exec(code_output)