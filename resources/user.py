from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message": "User with that username already exists."}, 400
        else:
            user = UserModel(data['username'], data['password'])
            user.save_to_db()
            return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200