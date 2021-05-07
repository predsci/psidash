from omegaconf import OmegaConf
from importlib import import_module
from dash.dependencies import Input, Output, State, MATCH, ALL

from collections import namedtuple


def load_conf(conf_file):
    return OmegaConf.to_container(OmegaConf.load(conf_file), resolve=True)


# +
def load_class(component):
    """accepts dictionary or str"""
    try: 
        if isinstance(component, dict):
            class_name = component['class']       
        else:
            class_name = component

    except:
        raise ImportError('could not parse class from {}'.format(component))
        
    class_parts = class_name.split('.')
    module_name = '.'.join(class_parts[:-1])
    class_name = class_parts[-1]

    try:
        return getattr(import_module(module_name), class_name)
    except:
        raise ImportError('cannot import {} from {}'.format(class_name, module_name))

def load_components(conf_):
    """class based component loader"""
    if 'class' in conf_:
        class_ = load_class(conf_)
        kwargs = {k:conf_[k] for k in conf_ if k not in ['class', 'children']}
        children = conf_.get('children')
        if children is not None:
            if isinstance(children, str):
                pass
            else:
                children_ = []
                for child in children:
                    children_.append(load_components(child))
                children = children_
        return class_(children=children, **kwargs)
    else:
        return conf_
        # raise IOError('conf has no class {}'.format(list(conf_)))



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

def load_dash(name, conf):
    dash_class = load_class(conf)
    kwargs = {k:conf[k] for k in conf if k not in ['class']}
    return dash_class(name, **kwargs)

# +
            

        

def is_dot_config(conf_):
    if isinstance(conf_, dict):
        if len(conf_) == 1:
            for name, kwargs in conf_.items():
                if '.' in name:
                    return True
    return False

def instantiate_conf(conf_):
    for class_name, kwargs in conf_.items():
        class_ = load_class(class_name)
        if isinstance(kwargs, dict):
            print('found dict {}'.format(kwargs))
            return class_(**instantiate_conf(kwargs))
        else:
            print('not a dict {}'.format(kwargs))
            return class_(kwargs)

def load_dot_components(conf_):
    """dot based component loader"""
    if is_dot_config(conf_):
        print('found dot config')
        for name, val in conf_.items():
            class_ = load_class(name)
            if isinstance(val, dict):
                print('{} has dict val'.format(name))
                if is_dot_config(val):
                    obj = load_dot_components(val)
                else:
                    print('{} not a dot config'.format(val))
                    obj = class_(**val)
                return obj
            elif isinstance(val, list):
                print('{} list val'.format(name))
                return class_(*val)
            else:
                print('found {}'.format(type(val)))
                return class_(val)
                
    else:
        print("not a dot config")

    if isinstance(conf_, list):
        print('found list')
        return [load_dot_components(_) for _ in conf_]

    

# +
def test_dot_conf_dict():
    greeting = {
        'dash_html_components.Div': dict(id = 'you_guys', children=['hey', 'you'])}
    return load_dot_components(greeting)

test_dot_conf_dict()


# -

def test_dot_conf_list():
    return load_dot_components({'dash_html_components.Div': ['hey', 'you']})
test_dot_conf_list()


def test_dot_conf_nested():
    return load_dot_components(
        {'dash_html_components.Div': {'children': ['hey', {'dash_html_components.Div':['you']}]}}
    )
test_dot_conf_nested()

is_dot_config({'dash_html_components.Div':['you']})



