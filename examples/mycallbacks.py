import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

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


def show_workflow_summary(n_clicks):
    # print(n_clicks, data)
    is_open = n_clicks % 2 == 0
    if n_clicks %2:
        style = dict(color= 'red')
    else:
        style = dict(color='blue')
    children = [
        html.Summary("number of children:"),
        html.Div("{} children!".format(n_clicks))]
    return is_open, style, children



