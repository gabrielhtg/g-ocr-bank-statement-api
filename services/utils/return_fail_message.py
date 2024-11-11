from errno import errorcode
from flask import jsonify


def returnFailMessage(message: str, errorCode: int) :
    return jsonify({
        'success' : False,
        'data' : message
    }), errorCode