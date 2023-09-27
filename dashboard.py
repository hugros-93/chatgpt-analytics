from dash import Dash, html, dcc, dash_table
import json
import re
import os
import plotly
import pandas as pd

def load_chatgpt_prompt():
    filename = 'input_prompt/input_prompt.txt'
    with open(filename, "r") as f:
        input_prompt = f.read()
    return f'"_{input_prompt}_"'

def load_input_data():
    filename = 'input_data/input_data.csv'
    df = pd.read_csv(filename)
    df = df.iloc[:10, :]
    return df

def load_chatgpt_code():
    filename = 'output_chatgpt/output_chatgpt.json'
    with open(filename, "r") as f:
        response = json.load(f)
    chatgpt_response = response["choices"][0]["message"]["content"]
    pattern = r'```python(.*?)```'
    code_blocks = re.findall(pattern, chatgpt_response, re.DOTALL)
    code_output = "\n".join([x.strip() for x in code_blocks])
    code_output = '```python\n' + code_output + '\n```'
    return code_output

def load_chatgpt_chart():
    dir = 'output_charts/'
    list_plotly_charts = []
    for f in os.listdir(dir):
        fig = plotly.io.read_json(f'{dir}/{f}')
        list_plotly_charts.append(fig)
    return list_plotly_charts

app = Dash(__name__)

# Get data
input_data = load_input_data()
chatgpt_input_prompt = load_chatgpt_prompt()
chatgpt_code_response = load_chatgpt_code()
chatgpt_charts = load_chatgpt_chart()
chatgpt_charts = [dcc.Graph(figure=chart) for chart in chatgpt_charts]

# Dashboard
app.layout = html.Div([
    html.H1('ChatGPT 4 Analytics', style={'textAlign':'center'}),
    html.Div([
        html.H2("Input data"),
        dash_table.DataTable(data=input_data.to_dict('records'), style_table={'overflowX': 'auto'}),
        html.H2("Input prompt"),
        dcc.Markdown(chatgpt_input_prompt),
        html.H2("ChatGPT answer"),
        dcc.Markdown(chatgpt_code_response)
    ], style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        html.H2("ChatGPT Charts"),
        html.Div(chatgpt_charts)
    ], style={'width': '70%', 'float': 'right', 'display': 'inline-block'}),  
    ]
)

if __name__ == '__main__':
    app.run(debug=True)