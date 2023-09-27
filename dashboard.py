from dash import Dash, html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc
import json
import re
import os
import plotly
import pandas as pd
from datetime import datetime, timedelta
from chatgpt_analytics import ask_chat_gpt, plot_from_response

def load_chatgpt_prompt():
    filename = 'input_prompt/input_prompt.txt'
    with open(filename, "r") as f:
        input_prompt = f.read()
    return f'"_{input_prompt}_"'

def load_input_data():
    filename = 'input_data/input_data.csv'
    df = pd.read_csv(filename)
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
        fig.update_layout(height=600)
        list_plotly_charts.append(fig)
    return list_plotly_charts

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Get input data
input_data = load_input_data()

# Dashboard
app.layout = html.Div([
    html.H1('ChatGPT 4 Analytics', style={'textAlign':'center'}),
    html.Div([
        html.H2("Input data"),
        dash_table.DataTable(data=input_data.to_dict('records'), style_table={'overflowX': 'auto', 'width': '100%', 'height': 300}),
        html.H2("ChatGPT prompt"),
        dcc.Input(id='prompt-text-input', type='text', placeholder='Enter ChatGPT prompt here', style={'width': '100%', 'height': 50}),
        html.Div([
            html.Button(id='submit-button-state', children='Submit', style={'width': '10%', 'float': 'left', 'display': 'inline-block'}),
            dcc.Loading(
                id="loading-status",
                type="dot",
                children=html.Div(id="loading-status-output"),
                style={'width': '10%', 'float': 'right', 'display': 'inline-block'}
            ),
        ], style={'width': '100%', 'float': 'centered', 'display': 'inline-block', 'height': 75}),
    ], style={'width': '100%', 'float': 'centered', 'display': 'inline-block'}),
    html.Div([
        html.H2("Input prompt"),
        dcc.Markdown(id='prompt-text-output', children='Loading last results...'),
        html.H2("ChatGPT answer"),
        dcc.Markdown(id='chatgpt-code-output', children='Loading last results...')
    ], style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        html.H2("ChatGPT Charts"),
        html.Div(id='chatgpt-charts-output', children='Loading last results...')
    ], style={'width': '70%', 'float': 'right', 'display': 'inline-block'}),  
    ]
)

# Callback
@callback(
    Output("loading-status-output", "children"),
    Output("prompt-text-output", "children"),
    Output("chatgpt-code-output", "children"),
    Output("chatgpt-charts-output", "children"),
    Input('submit-button-state', "n_clicks"),
    State("prompt-text-input", "value"),
)
def update_dashboard_on_click(_, prompt_text_input):
    if prompt_text_input == None or prompt_text_input == '':
        chatgpt_input_prompt = load_chatgpt_prompt()
        chatgpt_code_response = load_chatgpt_code()
        chatgpt_charts = load_chatgpt_chart()
        chatgpt_charts = [dcc.Graph(figure=chart) for chart in chatgpt_charts]
        status = f'Ready! ✅'
        return status, chatgpt_input_prompt, chatgpt_code_response, chatgpt_charts
    else:
        time_to_update = datetime.now()
        response = ask_chat_gpt(prompt_text_input)
        plot_from_response(response)
        chatgpt_input_prompt = load_chatgpt_prompt()
        chatgpt_code_response = load_chatgpt_code()
        chatgpt_charts = load_chatgpt_chart()
        chatgpt_charts = [dcc.Graph(figure=chart) for chart in chatgpt_charts]
        time_to_update = datetime.now() - time_to_update
        time_to_update = int(time_to_update.total_seconds())
        status = f'Done! ✅ ({time_to_update}s)'
        return status, chatgpt_input_prompt, chatgpt_code_response, chatgpt_charts

if __name__ == '__main__':
    app.run(debug=True)