from dash import Dash, html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc
import json
import re
import os
import plotly
import pandas as pd
import base64
import io
from datetime import datetime, timedelta
from chatgpt_analytics import ask_chat_gpt, plot_from_response

def load_chatgpt_prompt():
    filename = 'input_prompt/input_prompt.txt'
    try:
        with open(filename, "r") as f:
            input_prompt = f.read()
    except:
        input_prompt = ''
    return input_prompt

def load_input_data(contents, filename, date):
    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    df.to_csv('input_data/input_data.csv')
    return df

def load_chatgpt_code():
    filename = 'output_chatgpt/output_chatgpt.json'
    try:
        with open(filename, "r") as f:
            response = json.load(f)
        chatgpt_response = response["choices"][0]["message"]["content"]
        pattern = r'```python(.*?)```'
        code_blocks = re.findall(pattern, chatgpt_response, re.DOTALL)
        code_output = "\n".join([x.strip() for x in code_blocks])
        code_output = '```python\n' + code_output + '\n```'
    except:
        code_output = ''
    return code_output

def load_chatgpt_chart():
    dir = 'output_charts/'
    list_plotly_charts = []
    for f in os.listdir(dir):
        fig = plotly.io.read_json(f'{dir}/{f}')
        fig.update_layout(height=600)
        list_plotly_charts.append(fig)
    return list_plotly_charts

def clean_history():
    try:
        os.remove("output_chatgpt/output_chatgpt_history.json")
        os.remove("input_prompt/input_prompt.txt")
    except:
        print('Nothing to clean!')

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Dashboard
app.layout = html.Div([
    html.H1('ChatGPT Analytics', style={'textAlign':'center'}),
    html.Div([
        html.H2("Input data"),
        dcc.Markdown("_Please select `.csv` files only._"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '98%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '1%'
            },
            multiple=False
        ),
        dcc.Loading(
            id="loading-status-data",
            type="dot",
            children=dcc.Markdown(id="loading-status-data-output")
        ),
        html.Div(id='output-data-upload'),
        html.H2("ChatGPT prompt"),
        dcc.Input(id='prompt-text-input', type='text', placeholder='Enter ChatGPT prompt here', style={'width': '100%', 'height': 50}),
        html.Div([
            html.Button(id='submit-button-state', children='Submit'),
            dcc.Loading(
                id="loading-status",
                type="dot",
                children=dcc.Markdown(id="loading-status-output"),
                style={'width': '10%', 'float': 'right', 'display': 'inline-block'}
            ),
        ], style={'width': '100%', 'float': 'centered', 'display': 'inline-block', 'height': 75}),
    ], style={'width': '100%', 'float': 'centered', 'display': 'inline-block'}),
    html.Div([
        html.H2("Input prompt"),
        html.Button(id='clean-history-button', children='Clean history'),
        dcc.Markdown(id='prompt-text-output', children='...'),
        html.H2("ChatGPT answer"),
        dcc.Markdown('_Extracting `Python` code only._'),
        dcc.Markdown(id='chatgpt-code-output', children='...')
    ], style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        html.H2("ChatGPT Charts"),
        html.Div(id='chatgpt-charts-output', children='...')
    ], style={'width': '70%', 'float': 'right', 'display': 'inline-block'}),  
    ]
)

# Callbacks
@callback(
    Output("loading-status-data-output", "children"),
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(content, name, date):
    if content is not None:
        df = load_input_data(content, name, date)
        df = df.iloc[:1000, :]
        children = dash_table.DataTable(
            data=df.to_dict('records'), 
            style_table={
                'overflowX': 'auto', 
                'width': '100%', 
                'height': 350
            },
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            },
            sort_action="native",
            sort_mode="multi",
            page_size= 10
        )
        status = f'_Loaded! ✅_'
        return status, children
    else:
        filename = 'input_data/input_data.csv'
        try:
            df = pd.read_csv(filename)
            df = df.iloc[:1000, :]
            children = dash_table.DataTable(
                data=df.to_dict('records'), 
                style_table={
                    'overflowX': 'auto', 
                    'width': '100%', 
                    'height': 350
                },
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'fontWeight': 'normal'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'normal'
                },
                sort_action="native",
                sort_mode="multi",
                page_size= 10
            )
            status = f'_Loaded! ✅_'
        except:
            status = ''
            children = html.P('')
        return status, children

@callback(
    Output("loading-status-output", "children"),
    Output("prompt-text-output", "children"),
    Output("chatgpt-code-output", "children"),
    Output("chatgpt-charts-output", "children"),
    Input('submit-button-state', "n_clicks"),
    State("prompt-text-input", "value")
)
def update_dashboard_on_click(_, prompt_text_input):
    if prompt_text_input == None or prompt_text_input == '':
        chatgpt_input_prompt = load_chatgpt_prompt()
        chatgpt_code_response = load_chatgpt_code()
        chatgpt_charts = load_chatgpt_chart()
        chatgpt_charts = [dcc.Graph(figure=chart) for chart in chatgpt_charts]
        status = ''
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
        status = f'_Done! ✅ ({time_to_update}s)_'
        return status, chatgpt_input_prompt, chatgpt_code_response, chatgpt_charts
    
@callback(
    Output("prompt-text-output", "children", allow_duplicate=True),
    Input('clean-history-button', "n_clicks"),
    prevent_initial_call=True
)
def update_clean_history(n_clicks):
    if n_clicks is not None:
        clean_history()
        chatgpt_input_prompt = load_chatgpt_prompt()
        return chatgpt_input_prompt

if __name__ == '__main__':
    app.run(debug=True)