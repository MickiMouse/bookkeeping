from app.models import User
from app.api import bp
from flask import request, jsonify


@bp.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    data = []
    for user in users:
        user_data = dict()
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['pass_hash'] = user.pass_hash
        data.append(user_data)
    return jsonify(data)


@bp.route('/api/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(int(user_id))
    data = dict()
    data['id'] = int(user_id)
    data['username'] = user.username
    data['email'] = user.email
    data['pass_hash'] = user.pass_hash
    return jsonify({'user': data})
