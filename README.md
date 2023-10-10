# `chatgpt-analytics`: automate analytics with ChatGPT 

![Screenshot](image.png "Screenshot")

## Installation 💾
- Clone the repository
- Create a `venv` using the `requirements.txt`.
- Create a ChatGPT account and an API key, and add a text file `API_KEY.txt` in the root folder with your ChatGPT API key.
- Run the dashboard in command line: `> python dashboard.py`. 
- Open local host `http://127.0.0.1:8050` in navigator to access the dashboard.

## Using the dashboard 📊
- Load `.csv` data using drag and drop, or click `Select files` to select files in folder.
- Enter prompt describing the chart you want to have from the input data, and click `Submit` to generate the chart.
- The code to generate the chart will be seen in the `ChatGPT answer` section.
- Refine demande by adding new prompts, the history of demand being seen under the submit button.
- Click `Clean history` in order to reset context for ChatGPT.

## Project structure 📂

### Files
- `chatgpt_analytics.py`: python file with alll functions to tinteract with ChatGPT.
- `dashboard.py`: python file for interactive dahsboard and visualizations.
- `generate_data.py`: generate synthetic data in the `input_data/` folder. _Not usefull to run the project with your own data._
- `prompt_context.txt`: context prompt file for ChatGPT.
= `requirements.txt`: packages to create the venv.

### Folders
- `input_data/`: folder where the loaded input data will be stored.
- `input_prompt/`: history of prompt entered in the session.
- `output_charts/`: plotly charts as `.json` files exported from the chatgpt answer.
- `output_chatgpt/`: `.json` files of the history of chatgpt answers and last one.