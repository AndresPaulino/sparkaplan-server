from models.user import User
from flask import jsonify

class UserController:
    @staticmethod
    def update_user(data):
        user = User.find_by_email(data['email'])
        if not user:
            return jsonify({"message": "User not found"}), 404

        display_name = data.get('first_name', user.first_name) + " " + data.get('last_name', user.last_name)

        user.update(
            first_name=data.get('first_name', user.first_name),
            last_name=data.get('last_name', user.last_name),
            state=data.get('state', user.state),
            county=data.get('county', user.county),
            display_name=display_name
        )
        
        return jsonify({"message": "User details updated successfully"}), 200
