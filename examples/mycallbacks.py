import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash
import json

def pass_through(*args):
	return args

def render_sum(x, op, y):
    if op == 'plus':
        return x + y
    elif op == 'minus':
        return x - y
    elif op == 'multiply':
        return x*y
    elif op == 'divide':
        return x/y

def display_dropdowns(n_clicks, workflow, children):
    """create stateful dynamic dropdowns
    see Simple Example with MATCH https://dash.plotly.com/pattern-matching-callbacks
    """
    if workflow == 'city':
        new_element = html.Div([
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dropdown',
                    'index': n_clicks
                },
                options=[{'label': i, 'value': i} for i in ['NYC', 'MTL', 'LA', 'TOKYO']],
                value='NYC'
            ),
            html.Div(
                id={
                    'type': 'dynamic-output',
                    'index': n_clicks
                }
            )
        ])
        
    elif workflow == 'state':
        new_element = html.Div([
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dropdown',
                    'index': n_clicks
                },
                options=[{'label': i, 'value': i} for i in ['MA', 'CA', 'TX', 'NY']],
                value='TX'
            ),
            html.Div(
                id={
                    'type': 'dynamic-output',
                    'index': n_clicks
                }
            )
        ])
    else:
        raise PreventUpdate

    children.append(new_element)

    return children


def display_output(value, id):
    return html.Div('Dropdown {} = {}'.format(id['index'], value))

def get_triggered():
    """retrieve id of the triggered element"""
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return json.loads(button_id)


def show_workflow_summary(tab_id):
    workflow_summary = "This is the summary for {}".format(tab_id)
    return workflow_summary

def show_workflow_functions(tab_id):
    styles = list()
    for _ in dash.callback_context.outputs_list:
        if _['id']['id'] == int(tab_id):
            styles.append(dict(display='block'))
        else:
            styles.append(dict(display='none'))
    return styles

def update_workflow_functions(style, workflow_state):
    if style['display'] == 'none':
        raise PreventUpdate

    function_area = get_triggered()

    function_key = 'functions-{}'.format(function_area['id'])
    function_children =[]
    if function_key in workflow_state:
        for _ in workflow_state[function_key]:
            function_children.append(html.Div(_))

    return function_children




