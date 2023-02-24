from flask_restx import Namespace,Resource,fields
from ..models import User
from flask import request
from ..utils import db
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
auth_namespace=Namespace("auth",description="auth api")
signup_model=auth_namespace.model("signup",{
    'id':fields.Integer(),
    'username':fields.String(required=True,description="A username"),
    'email':fields.String(required=True,description="an email"),
    "password":fields.String(required=True,description="a password")
})
login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'is_active': fields.Boolean(description="This shows if a User is active or not"),
        'is_staff': fields.Boolean(description="This shows that if a User is a member of staff")
    }
)
@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model,envelope='resource')
    def post(self):
        data=request.get_json()
        new_user=User(username=data.get("username"),
        email=data.get("email"),password_hash=generate_password_hash(data.get("password")))
        db.session.add(new_user)
        db.session.commit()
        return new_user,201

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user  and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response,200
@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}