* answering issue 1

> so In my case id type of both the element can not be same. otherwise for there will be error.

Other keywords in the `id` dictionary may be different, as long as the keyword connected to `MATCH` is the same. In the example below, all ids use the `index` keyword, but they have different `type` keywords:

```yaml
input:
  - id:
      type: custom-workflow
      index: MATCH
    attr: value
output:
  - id:
      type: workflow-summary
      index: MATCH
    attr: children
  - id:
      type: function-area
      index: MATCH
    attr: style
  - id:
      type: function-list
      index: MATCH
    attr: children
```

I have updated the workflows.yaml in this repo to be better match your use case: a tabs component that triggers a summary render, a style update on a function wrapper, which triggers updates to function lists. You should be able to run it like this:

```sh
cd examples
python workflows.py
```

<details>
  <summary> Click here to see the full layout </summary>

```yaml
layout:
  html.Div:
    children:
      - dbc.Card:
          children:
          - dcc.Tabs:
              id: tabs
              children:
                - dcc.Tab:
                    label: Tab 1
                    value: '1'
                - dcc.Tab:
                    label: Tab 2
                    value: '2'
              value: '1' # must be a string
          - html.Div:
              id: workflow-summary
              children: empty
          style:
            width: 18rem
      - dbc.Card:
          children:
          - html.Div:
              id:
                type: function-area
                id: 1
              style:
                display: block
                # display: none # or 'block' to reveal
              children:
                - html.Div:
                    id:
                      type: workflow-functions
                      id: 1
                    children: no children yet for 1
          - html.Div:
              id:
                type: function-area
                id: 2
              style:
                display: block
                # display: none # or 'block' to reveal
              children:
                - html.Div:
                    id:
                      type: workflow-functions
                      id: 2
                    children: no children yet for 2
          style:
            width: 18rem
      - dcc.Store:
          id: workflow-list-store
          data:
            functions-1:
              - f(x) = x**2-x-1
              - f(y) = cos(y)
            functions-2:
              - f(y) = sin(y)
              - f(g) = g**2

```
</details>

I've split things up into multiple callbacks

```yaml
  show_workflow_summary:
    input:
      - id: tabs
        attr: value
    output:
      - id: workflow-summary
        attr: children
    callback: mycallbacks.show_workflow_summary
```

This one simply updates a single workflow summary div based on which tab is currently active.

```yaml
  show_workflow_functions:
    input:
      - id: tabs
        attr: value
    output:
      - id: 
          type: function-area
          id: ALL
        attr: style
    callback: mycallbacks.show_workflow_functions
```
This is a bit more complex: it updates all elements with `type: function-area` at the same time. However, inside the `mycallbacks.show_workflow_functions` we check to see which of those outputs needs to be visible:

```python
    for _ in dash.callback_context.outputs_list:
        if _['id']['id'] == int(tab_id):
            styles.append(dict(display='block'))
        else:
            styles.append(dict(display='none'))
```

Finally, the function lists are updated by matching with their parent div based on its visibility:

```yaml
  update_workflow_functions:
    input:
      - id:
          type: function-area
          id: MATCH
        attr: style
    output:
      - id:
          type: workflow-functions
          id: MATCH
        attr: children
    state:
       - id: workflow-list-store
         attr: data
    callback: mycallbacks.update_workflow_functions
```
and here we check if the parent is visible before updating the children:
```python
def update_workflow_functions(style, workflow_state):    
    if style['display'] == 'none':
        raise PreventUpdate
```



## 2021-11-01 11:12:14.258405: clock-in

## 2021-11-01 11:04:15.048513: clock-out


## 2021-11-01 10:53:17.953771: clock-in

## 2021-10-27 20:49:37.945847: clock-out

* multi attribute match

## 2021-10-27 19:14:16.294791: clock-in

## 2021-10-27 14:06:40.275888: clock-out

* troubleshooting muiltiple attribute issue

## 2021-10-27 13:54:25.513307: clock-in

## 2021-10-27 00:49:03.367522: clock-out

* trying to use multiple MATCH values

## 2021-10-27 00:40:37.039513: clock-in

## 2021-10-27 00:34:33.876537: clock-out

* allow other id keys to use MATCH and ALL

## 2021-10-26 23:27:24.699474: clock-in

* cleaning up examples

## 2021-05-14 15:18:26.617027: clock-out

* added install instructions

## 2021-05-14 15:14:36.851582: clock-in

## 2021-05-13 17:37:43.499985: clock-out

* skipping hydra for hot reloading

* this works, but needs interval to refresh `gunicorn psidash.cli.main:server -b 0.0.0.0:8050 --reload --reload-extra-file psidash.yaml`
* allowed generation of server variable outside of main loop
* merging doesn't work with dot keywords. Example after merge:

```yaml
  dash.Dash:
    title: psidash basic
  jupyter_dash.JupyterDash:
    external_scripts: ${external_scripts}
    external_stylesheets: ${external_stylesheets}
    title: psidash
```

`dash.Dash` contents won't replace jupyter_dash.JupyterDash

## 2021-05-13 15:56:01.161331: clock-in

## 2021-05-12 18:29:35.791931: clock-out

* adding command line tool

## 2021-05-12 17:12:47.414452: clock-in

## 2021-05-11 17:15:33.523594: clock-out

* using new class dict syntax

## 2021-05-11 17:07:02.202455: clock-in

## 2021-05-11 16:55:49.763731: clock-out

* improved conf syntax, removed superfluous class keyword

## 2021-05-11 14:15:40.659822: clock-in

## 2021-05-07 18:36:04.714902: clock-out

* dot config tests

## 2021-05-07 17:52:33.644595: clock-in

## 2021-05-07 17:25:25.062441: clock-out

* adding dot config

## 2021-05-07 15:34:16.593435: clock-in

* moving conf up
## 2021-05-06 10:18:08.736571: clock-out

* moving conf into details
* moving callback demo to readme

## 2021-05-06 09:46:42.579395: clock-in

## 2021-05-06 00:46:45.402471: clock-out

* updating readme
* removing notebook in favor of markdown
* syncing markdown
* layout demo matching official plotly docs

## 2021-05-05 22:30:52.154170: clock-in

## 2021-05-05 15:06:45.258942: clock-out

* ignoring dev files
* cleaned up install

## 2021-05-05 13:00:16.563345: clock-in

## 2021-05-05 11:33:20.645548: clock-out

* storing callbacks in namedtuple, added bootstrap

## 2021-05-05 10:59:52.965222: clock-in

## 2021-05-05 10:57:22.433866: clock-out


## 2021-05-05 10:38:36.543471: clock-in

## 2021-05-04 18:01:51.122513: clock-out

* creating lambda signature

## 2021-05-04 17:01:37.235238: clock-in

## 2021-05-04 15:12:51.305971: clock-out

* added demo loading dash app from config
* running docker-compose from `report-generator/Docker/docker-compose.yaml`
* note: predscinc should generate a `docker-compose.yaml`

# 2021-05-04 13:36:55.133535: clock-in: T-10m 

