# +
from psidash import load_app

app = load_app(__name__, 'workflows.yaml')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, mode='external', debug=True)

server = app.server


