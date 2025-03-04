from flask import Flask, request
import uuid
from db.user import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import SuccessMessageSchema, UserSchema, UserQuerySchema
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST


blp = Blueprint("users", __name__, description="Operations on Users")

@blp.route("/login")
class UserLogin(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UserSchema)
    def post(self, request_data):

        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        # check if user exits in the database
        user_id = self.db.verify_user(username, password)
        if user_id:
            return {
                "access_token" : create_access_token(identity=user_id)
            }
        abort(400, message="Username or Password Incorrect!")

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out!"}

@blp.route("/user")
class Users(MethodView):

    def __init__(self):
        self.db = UserDatabase()
    
    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def get(self, args):
        id = args.get("id")
        result = self.db.get_user(id)
        if result is None:
            abort(404, message="User doesn't exit!")
        return result

    @blp.arguments(UserSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, request_data):
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        print(len(password))
        if self.db.add_user(username, password):
            return {"message": "User added successfully"}, 201
        return abort(403, message="User already exits!")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        if self.db.delete_user(id):
            return {"message" : "User deleted successfuly"}, 200
        abort(404, message="Given user Not found!")