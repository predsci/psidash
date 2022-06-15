from psidash.psidash import load_app

app = load_app(__name__, 'plotly_intro.yaml')

if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=True,
        extra_files=['plotly_intro.yaml'])
