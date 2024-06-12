from flask import Blueprint, jsonify
from ..utils import Utils
from ..config.db import db_connection

bp = Blueprint('scrape', __name__)

@bp.route('/store', methods=['GET'])
def get_data():
    utils = Utils()
    db = db_connection('scrapes')

    data = utils.scrape_data()

    result = db.insert_many(data)

    response = {
        'status':'success',
        'message':'Success Scrape and Store Data',
    }
    
    return jsonify(response), 200