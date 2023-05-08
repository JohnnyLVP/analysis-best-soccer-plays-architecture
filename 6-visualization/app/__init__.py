from flask import Flask


def create_app():
    app = Flask(__name__)
    prefix = ''

    # a simple response that returns OK
    @app.route(prefix + '/')
    def send_ok():
        return 'OK'

    return app
