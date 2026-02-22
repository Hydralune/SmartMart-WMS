from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': '用户名或密码错误'}), 401
    token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'username': user.username}
    )
    return jsonify({'token': token, 'user': user.to_dict()})
