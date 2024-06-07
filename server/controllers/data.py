from flask import Blueprint, jsonify

bp = Blueprint('data', __name__)

@bp.route('/', methods=['GET'])
def get_data():
    data = {
        'status':'success',
        "message": 'Success Get Test Data',
        'data': [
            {
            'id':'09090909',
            'title':'Lorem Ipsum'
        },
        {
            'id':'08080808080',
            'title':'Dolor Smit'
        }
        ]
    }

    return jsonify(data), 200