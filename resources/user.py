from flask_restful import Resource, reqparse
from hmac import compare_digest
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be empty"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be empty")


class UserRegister(Resource):
    TABLE_NAME = 'users'

    def post(self):
        data = _user_parser.parse_args()
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


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials...'}, 401
