from flask import Blueprint, request
from controllers.user_controller import UserController

user_view = Blueprint('user', __name__)

@user_view.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    return UserController.update_user(data)
