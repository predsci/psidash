
import hydra
from hydra import utils
from os import path
import os
from omegaconf import OmegaConf
from psidash import load_dash, load_components, load_conf, assign_callbacks, get_callbacks
import sys

def config_override(cfg):
    """Overrides with user-supplied configuration

    kamodo will override its configuration using
    kamodo.yaml if it is in the current working directory
    or users can set an override config:
        config_override=path/to/myconfig.yaml
    """
    override_path = hydra.utils.to_absolute_path(cfg.config_override)
    if path.exists(override_path):
        if cfg.verbose > 1:
            print('found override {}'.format(override_path))
        override_conf = OmegaConf.load(override_path)
        # merge overrides first input with second
        cfg = OmegaConf.merge(cfg, override_conf)
    else:
        if cfg.verbose > 1:
            print('no override config found {}'.format(cfg.config_override))
    return cfg

def setup_app(conf):
    print('app kwargs', conf['app'])
    app = load_dash(__name__, conf['app'], conf.get('import'))
    app.layout = load_components(conf['layout'], conf.get('import'))
    
    if 'callbacks' in conf:
        callbacks = get_callbacks(app, conf['callbacks'])
        assign_callbacks(callbacks, conf['callbacks'])
    return app


@hydra.main(config_path='conf/config.yaml', strict=False)
def main(cfg):
    override_path = hydra.utils.to_absolute_path(cfg.config_override)
    if path.exists(override_path):
        cfg = OmegaConf.load(override_path)
    
    if cfg.verbose > 1:
        print(cfg.pretty())

    conf = OmegaConf.to_container(cfg, resolve=True)
    app = setup_app(conf)
    app.run_server(**conf['run_server'])


if __name__ == "__main__":
    print('i have entered from main')
    main()
else:
    # importing from gunicorn
    # find the configuration file
    print('loading conf from {}'.format(os.getcwd()))
    print(__name__)
    config_file = 'psidash.yaml'
    if path.exists(config_file):
        print('found psidash')
        cfg = OmegaConf.load(config_file)
        conf = OmegaConf.to_container(cfg, resolve=True)
        app = setup_app(conf)
        server = app.server

# entrypoint for package installer
def entry():
    app.run_server(**conf['run_server'])




