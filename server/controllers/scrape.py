import json
from flask import Blueprint, jsonify
from ..utils import Utils

bp = Blueprint('scrape', __name__)

@bp.route('/', methods=['GET'])
def get_data():
    utils = Utils()

    data = utils.scrape_data()
    response = {
        'status':'success',
        'message':'Success Scrap Data',
        'data':data
    }
    
    return jsonify(response), 200