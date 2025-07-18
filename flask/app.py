import os

from flask import Flask, request, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.items import blp as ItemBlueprint
from resources.stores import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.users import blp as UserBlueprint

from datetime import datetime, timedelta
from models import BlockedTokensModel


from flask_jwt_extended import verify_jwt_in_request
from flask import request

from db import db
import models

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CTK-shop REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "21857596912856177657044693095400912919"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def exipred_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message" : "The token expired", "error":"token_expired"}),
            401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message" : "Signature verification failed", "error":"Invalid_token"}),
            401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
         return(
            jsonify({"message" : "Request does not contain an access token", "error":"Invalid_token"}),
            401
        )
    
    #TODO globani protection za token
    # @app.before_request
    # def global_jwt_protect():
    #     # You can whitelist some public routes:
    #     print("print mojjj", request.endpoint)
    #     if request.endpoint in ('Users.UserLogin'):
    #         return
    #     verify_jwt_in_request() # verifikacij??


    # ovo ce napraviti sve tablice u bazi i relacije
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)


    # def delete_expired_tokens():
    #     expiration_time = datetime.utcnow() - timedelta(days=1)
    #     deleted = BlockedTokensModel.query.filter(BlockedTokensModel.created_at < expiration_time).delete()
    #     db.session.commit()
    #     print(f"Deleted {deleted} expired tokens.")

    # delete_expired_tokens()    
    
    return app


