from psidash import load_app

app = load_app(__name__, 'basic.yaml')

if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0', # needed for containers
        port=8050,
        mode='inline',
        debug=True,
        extra_files=['basic.yaml'])
