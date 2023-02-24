from flask import Flask
from flask_restx import Api
from .order import order_namespace
from .auth import auth_namespace
from .config.config import config_dict
from .utils import db
from .models import User,Order
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed
def create_app(config=config_dict["dev"]):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate=Migrate(app,db)
    jwt=JWTManager(app)
    api=Api(app)

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace)
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404
    @app.shell_context_processor
    def make_shell():
        return{
            "db":db,
            "user":User,
            "order":Order
        }
    return app