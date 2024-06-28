from flask import Blueprint, jsonify
from ..config.db import db_connection
from datetime import datetime

bp = Blueprint('data', __name__)

@bp.route('/scrape', methods=['GET'])
def get_data():
    # db = db_connection('scrapes')

    # today = datetime.now().strftime("%Y-%m-%d")
    # response = list(db.find({'date_added': today}))
    
    # for item in response:
    #     db.update_one({'kode_tender': item['kode_tender']},{'$set':{'is_show':False}})

    return jsonify({
        'status': 'Success'
    }), 200