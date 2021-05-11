from omegaconf import OmegaConf
from importlib import import_module
from dash.dependencies import Input, Output, State, MATCH, ALL

from collections import namedtuple


# ## Configuration

# We use OmegaConf to resolve yaml. This allows users to reference variables in `${}` notation

def load_conf(conf_file):
    return OmegaConf.to_container(OmegaConf.load(conf_file), resolve=True)

# ## Layout
#
# We want to support the following layout:
#
# ```yaml
# # import namespaces may be referenced by classes
# import:
#     dcc: dash_core_components
#
# header: # a custom variable
#     dcc.H4('header')
#     
# layout: # a special variable we'll look for
#     dcc.Div:
#         children:
#             - ${header} # OmegaConf will resolve
#             - dcc.Div('hi')
# ```


def load_class(component, module_names = None):
    """accepts dictionary or str"""
    try: 
        if isinstance(component, dict):
            raise NotImplementedError('removing')
            class_name = component['class']       
        else:
            class_name = component

    except:
        raise ImportError('could not parse class from {}'.format(component))

    class_parts = class_name.split('.')
        
    if module_names is not None:
        module_base = class_parts[0]
        for _ in module_names:
            if _ == module_base:
                class_parts[0] = module_names[_]
        
    module_name = '.'.join(class_parts[:-1])
    class_name = class_parts[-1]

    try:
        return getattr(import_module(module_name), class_name)
    except:
        raise ImportError('cannot import {} from {}'.format(class_name, module_name))


# +
def load_components(conf, module_names = None):
    if isinstance(conf, dict):
        for k,v in conf.items():
            if '.' in k:
                class_ = load_class(k, module_names)
                if isinstance(v, dict):
                    kwargs = dict()
                    for k_, v_ in v.items():
                        if k_ == 'children':
                            v_ = load_components(v['children'], module_names)
                        kwargs[k_] = v_
                    return class_(**kwargs)
                elif isinstance(v, list):
                    return class_(*v)
                else:
                    return class_(v)
    elif isinstance(conf, list):
        children = [load_components(child, module_names) for child in conf]
        return children
    else:
        return conf
    
def test_nested():
    load_components({'html.Div':
                  {'children':
                   [{'html.H4':'Hello Title'},
                    {'html.Div': 'there'}]
                  }
                 },
                 {'html': 'dash_html_components'} # imports
                )


# +
def get_match_type(id_):
    """Look for match key in callback id property
    see https://dash.plotly.com/pattern-matching-callbacks
    """
    match_types = dict(MATCH=MATCH, ALL=ALL)
    if isinstance(id_, dict):
        type_id = id_.get('id')
        if type_id in match_types:
            id_['id']=match_types[type_id]
    return id_

def get_callbacks(app, conf):
    # get the callback signatures
    signatures = {}
    component_types = dict(output=Output, input=Input, state=State)
    for k, v in conf.items():
        signature = []
        for type_ in 'output', 'input', 'state':
            components = v.get(type_)
            if components is not None:
                for _ in components:
                    try:
                        id_ = get_match_type(_['id'])
                    except:
                        print('problem with {} {} {}'.format(k, components, _))
                        raise

                    signature.append(component_types[type_](id_, _['attr']))
        signatures[k] = app.callback(*signature)
    signatures = namedtuple('Signatures', signatures)(**signatures)
    return signatures

def assign_callbacks(signatures, conf):
    for k, v in conf.items():
        if 'callback' in v:
            func = load_class(v['callback'])
            getattr(signatures, k)(func)

def load_dash(name, conf, module_names = None):
    for class_, kwargs in conf.items():
        dash_class = load_class(class_, module_names)
        return dash_class(name, **kwargs)


# -

def load_app(name, filename):
    """Load the complete application - layout, signatures, callbacks"""
    conf = load_conf(filename)
    app = load_dash(name, conf['app'], conf.get('import'))
    app.layout = load_components(conf['layout'], conf.get('import'))

    if 'callbacks' in conf:
        callbacks = get_callbacks(app, conf['callbacks'])
        assign_callbacks(callbacks, conf['callbacks'])
    
    return app


