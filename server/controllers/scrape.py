from flask import Blueprint, jsonify
from ..utils import Utils
from ..config.db import db_connection
from datetime import datetime,timedelta

bp = Blueprint('scrape', __name__)

@bp.route('/', methods=['GET'])
def scrape_data():
    utils = Utils()
    data = utils.scrape_data()
    total_data = len(data)

    response = {
        'status':'success',
        'message':'Success Scrape Data',
        'total_data':total_data,
        'data':data
    }

    return jsonify(response), 200

@bp.route('/store', methods=['GET'])
def scrape_store_data():
    utils = Utils()
    db = db_connection('scrapes')

    data = utils.scrape_data()
    new_data = []

    # Change Status To Unvisible For All Anchor Data
    db.update_many({},{'$set':{'is_show':False}})

    for item in data:
        if not db.find_one({'kode_tender': item['kode_tender']}):
            new_data.append(item)
        else:
            # Change Status To Visible For Active Data
            db.update_one({'kode_tender': item['kode_tender']},{"$set":{'is_show':True}})

    if new_data:
        # Add New Data 
        db.insert_many(new_data)
        
    total_data_count = db.count_documents({})

    response = {
        'status': 'success',
        'message': 'Success Scrape and Store Data',
        'total_data_in_collection': total_data_count,
        'data_found': len(data),
        'new_data': len(new_data),
    }
    
    return jsonify(response), 200