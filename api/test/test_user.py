

import unittest
from .. import create_app
from ..utils import db
from ..models  import User
from ..config.config import config_dict

from werkzeug.security import generate_password_hash



class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_user_registration(self):

        data = {
            "username": "Test User",
            "email": "testuser@gmail.com",
            "password": "password"
        }

        signup_response = self.client.post('/auth/signup', json=data)

        user = User.query.filter_by(email='testuser@gmail.com').first()

        assert user.username == "Test User"

        assert signup_response.status_code == 201

    def test_user_login(self):
        data = {
            "email":"testuser@gmail.com",
            "password": "password"
        }
        login_response = self.client.post('/auth/login', json=data)

        assert login_response.status_code == 200