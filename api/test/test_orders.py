import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models import Order

class OrderTestCase(unittest.TestCase):
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

    def test_get_all_orders(self):
        token = create_access_token(identity="Test User")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/order/orders', headers=headers)

        assert response.status_code == 200

        assert response.json == []

    def test_order_placement(self):
        token = create_access_token(identity="Test User")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "size": "MEDIUM",
            "quantity": 1,
            "flavour": "BBQ Chicken"
        }

        response = self.client.post('/order/orders', json=data, headers=headers)

        order = Order.query.filter_by(id=1).first()

        assert order.flavour == "BBQ Chicken"

        assert order.quantity == 1

        assert response.status_code == 201
    def test_get_particular_order(self):
        order=Order(size="SMALL",
                    flavour="chilli",
                    quantity=2)
        db.session.add(order)
        db.session.commit()
        
        token=create_access_token(identity="Test User")
        headers={"Authorization":f"Bearer {token}"}
        response=self.client.get("/order/1",headers=headers)
        assert response.status_code==200
