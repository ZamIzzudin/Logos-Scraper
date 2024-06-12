from flask import Blueprint, jsonify
from ..utils import Utils
from ..config.db import db_connection

bp = Blueprint('scrape', __name__)

@bp.route('/', methods=['GET'])
def scrape_data():
    utils = Utils()
    data = utils.scrape_data()

    response = {
        'status':'success',
        'message':'Success Scrape Data',
        'data':data
    }

    return jsonify(response), 200

@bp.route('/store', methods=['GET'])
def scrape_store_data():
    utils = Utils()
    db = db_connection('scrapes')

    data = utils.scrape_data()
    new_data = []

    for item in data:
        if not db.find_one({'kode_tender': item['kode_tender']}):
            new_data.append(item)

    if new_data:
        db.insert_many(new_data)
        
    total_data_count = db.count_documents({})

    response = {
        'status': 'success',
        'message': 'Success Scrape and Store Data',
        'total_data_in_collection': total_data_count
    }
    
    return jsonify(response), 200