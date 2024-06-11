from flask import Blueprint, jsonify
from ..config.db import db_connection

bp = Blueprint('data', __name__)

@bp.route('/scrape', methods=['GET'])
def get_data():
    db = db_connection('scrapes')

    data = list(db.find())

    for item in data:
        item['_id'] = str(item['_id'])

    return jsonify(data), 200