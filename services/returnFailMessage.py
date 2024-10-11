from flask import jsonify


def returnFailMessage(taskStatus, message) :
    return jsonify({
        'success' : taskStatus,
        'data' : message
    }), 400