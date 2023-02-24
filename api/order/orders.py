from flask_restx import Namespace,Resource,fields
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models import Order,User
from ..utils import db

order_namespace=Namespace("order",description="order api")
order_model=order_namespace.model('order',{
    'id':fields.Integer(description='an id'),
    'size':fields.String(description='the size of the order',required=True,enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE'],),
    'order_status':fields.String(description='the order status',required=True,enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']
    )
    ,'flavour':fields.String(description='flavour of the order', required=True),
    'quantity': fields.Integer(description='Number of Pizzas')


})
@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self):

       
        """
            Get all orders

        """
        orders=Order.query.all()
        return orders,200
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
            Place an order
        """
        user_id=get_jwt_identity()
        # data=request.get_json()
        # new_order=Order(user_id=get_jwt_identity(),**data)
        data = order_namespace.payload
        neworder=Order(**data,user_id=user_id)
        db.session.add(neworder)
        db.session.commit()
        return neworder,201

        

@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):

        """
            Retrieve an order by ID
        """
        order=Order.query.get(order_id)
        return order,200

    def put(self, order_id):
        """
            Update an order by ID
        """
        data=order_namespace.payload
        order=Order.query.get(order_id)
        if order:
            order.size=data["size"]
            order.flavour=data["flavour"]
            order.quantity=data["quantity"]
        else:
            order=Order(id=order_id,**data)
        db.session.add(order)
        db.session.commit()



    def delete(self, order_id):
        """
            Delete an order by ID
        """
        order=Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_with(order_model)
    def get(self, user_id, order_id):

        """
            Get a user's specific order
        """
        user=User.query.get_or_404(user_id)
        
        order=Order.query.filter_by(id=order_id).filter_by(users_=user).first()
        return order
@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_list_with(order_model)
    def get(self,user_id):
        """
            Get all orders by a user
        """
        user=User.query.get(user_id)
        orders=user.orders
        return orders

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        """
            Update an order's status
        """
        pass