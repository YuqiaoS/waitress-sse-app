from flask import Flask
from flask_sse import sse
from waitress import serve
import logging


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SSE_REDIS_URL="redis://localhost:6379/0",
    )

    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    # sse respond
    @app.route('/hello')
    def hello():
        sse.publish(data="got msg :)")
        return "hello back"
        

    # regiser
    app.register_blueprint(sse, url_prefix='/stream')

    return app


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)-8s %(name)s %(message)s",
        level=logging.DEBUG,
    )
    
    flaskapp = create_app()
    serve(flaskapp, listen='*:9000', _quiet=False)
    # create_app().run(debug=True)
