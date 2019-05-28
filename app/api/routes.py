from app.api import bp
from flask import request, jsonify


@bp.route('/api', methods=['GET'])
def get_all_users():
    return jsonify({'message': 'YOU ARE HERE!'})


@bp.route('/api/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    return user_id
