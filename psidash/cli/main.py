
import hydra
from os import path
import os
from omegaconf import OmegaConf
from psidash import load_dash, load_components, load_conf, assign_callbacks, get_callbacks

def config_override(cfg):
    """Overrides with user-supplied configuration

    kamodo will override its configuration using
    kamodo.yaml if it is in the current working directory
    or users can set an override config:
        config_override=path/to/myconfig.yaml
    """
    override_path = hydra.utils.to_absolute_path(cfg.config_override)
    if path.exists(override_path):
        override_conf = OmegaConf.load(override_path)
        # merge overrides first input with second
        cfg = OmegaConf.merge(cfg, override_conf)
    else:
        if cfg.verbose > 1:
            print('no override config found {}'.format(cfg.config_override))
    return cfg



@hydra.main(config_path='conf/config.yaml', strict=False)
def main(cfg):
    cfg = config_override(cfg)
    if cfg.verbose > 1:
        print(cfg.pretty())

    print('my name is ' + __name__)

    conf = OmegaConf.to_container(cfg, resolve=True)


    app = load_dash(__name__, conf['app'], conf.get('import'))
    app.layout = load_components(conf['layout'], conf.get('import'))

    if 'callbacks' in conf:
        callbacks = get_callbacks(app, conf['callbacks'])
        assign_callbacks(callbacks, conf['callbacks'])

    app.run_server(host='0.0.0.0', port=8050, mode='inline', debug=True)

# entrypoint for package installer
def entry():
    print('i have entered from entry'+ os.getcwd())
    main()

if __name__ == "__main__":
    print('i have entered from main')
    main()