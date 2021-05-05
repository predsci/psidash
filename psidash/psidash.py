from omegaconf import OmegaConf
from importlib import import_module
from dash.dependencies import Input, Output, State, MATCH, ALL

from collections import namedtuple


def load_conf(conf_file):
    return OmegaConf.to_container(OmegaConf.load('demo.yaml'), resolve=True)


# +
def load_class(component):
    _ = component['class'].split('.')
    module_name = '.'.join(_[:-1])
    class_name = _[-1]
    try:
        return getattr(import_module(module_name), class_name)
    except:
        raise ImportError('cannot import {} from {}'.format(class_name, module_name))

def load_components(conf_):
    if 'class' in conf_:
        class_ = load_class(conf_)
        kwargs = {k:conf_[k] for k in conf_ if k not in ['class', 'children']}
        children = conf_.get('children')
        if children is not None:
            if isinstance(children, str):
                pass
            else:
                children = [load_components(child) for child in children]
        return class_(children=children, **kwargs)
    else:
        raise IOError('conf has no class {}'.format(list(conf_)))

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
                    id_ = get_match_type(_['id'])
                    signature.append(component_types[type_](id_, _['attr']))
        signatures[k] = app.callback(*signature)
    signatures = namedtuple('Signatures', signatures)(**signatures)
    return signatures

def load_dash(conf):
    dash_class = load_class(conf)
    kwargs = {k:conf[k] for k in conf if k not in ['class']}
    return dash_class(**kwargs)
