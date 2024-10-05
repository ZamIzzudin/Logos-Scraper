from flask import Flask, jsonify
from .controllers.scrape import scrape_store_data
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    @app.route('/', methods=['GET'])
    def default():
        data = {
            'message':'Welcome to LPSE Scrapper',
            'status': 'Successfully Connected'
        }
        return jsonify(data), 200


    @app.route('/manual-scrape', methods=['GET'])
    def scrape():
        response = scrape_store_data()
        return jsonify(response), 200

    return app

def start_scheduler(interval):
    # scheduler.add_job(func=scrape_store_data, trigger="interval", seconds=interval)
    # scheduler.add_job(func=scrape_store_data, trigger="interval", minutes=interval)
    scheduler.add_job(func=scrape_store_data, trigger="interval", hours=interval)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()