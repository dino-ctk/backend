from flask import Flask, request, jsonify
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort, Blueprint
from schemas import UserScheme
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, 
    get_jwt, 
    jwt_required,
    create_refresh_token,
    get_jwt_identity
)



from models import UserModel, BlockedTokensModel


blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserScheme)
    def post(self, user_data):
        # check if there is A user with that username
        if UserModel.query.filter(
             UserModel.username == user_data["username"]
        ).first():
             abort(409, message="A user with that username already exists")

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message":"User succesfully created"}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserScheme)
    def post(self, user_data):   
        user = UserModel.query.filter(
             UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=7))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid credentials") 

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        #dobiti token
        current_token = get_jwt()['jti']
        blockedtoken = BlockedTokensModel(token=current_token)
        db.session.add(blockedtoken)
        db.session.commit()
        return {"message": "User loged out"}, 200

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):  
        current_user = get_jwt_identity()  
        new_token = create_access_token(identity=current_user, fresh=False)
        current_token = get_jwt()['jti']
        blockedtoken = BlockedTokensModel(token=current_token)
        db.session.add(blockedtoken)
        db.session.commit()
        return {"access_token":new_token}, 200

@blp.route("/user/<int:user_id>")
class UserHelper(MethodView):
    @blp.response(200,UserScheme)
    def get(self, user_id):
        user =  UserModel.query.get_or_404(user_id)   
        return user
    
    def delete(self, user_id):
        user =  UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted."}, 200