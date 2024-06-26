from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    @app.route('/', methods=['GET'])
    def default():
        data = {
            'message':'Welcome to REST API',
            'created by': 'AyamIyudin & Welldone Ganteng'
        }
        return jsonify(data), 200

    with app.app_context():
        from .controllers import data, scrape
        app.register_blueprint(data.bp, url_prefix='/data')
        app.register_blueprint(scrape.bp, url_prefix='/scrape')

    return app