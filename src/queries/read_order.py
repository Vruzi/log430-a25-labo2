"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc, func
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from models.product import Product
from types import SimpleNamespace
import json

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    # TODO: écrivez la méthode
    r = get_redis_conn()
    
    order_keys = r.keys("order:*")
    orders = []
    
    for key in order_keys[:limit]:
        order_json = r.get(key)
        if order_json:
            order_dict = json.loads(order_json)
            order_obj = SimpleNamespace(**order_dict)
            orders.append(order_obj)
    
    orders.sort(key=lambda x: int(x.id), reverse=False)
    return orders

def get_highest_spending_users():
    """Get report of best selling products"""
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    session = get_sqlalchemy_session()
    return session.query(
        User.id,
        User.name,
        func.sum(Order.total_amount).label('total_spent')
    ).join(Order, User.id == Order.user_id)\
        .group_by(User.id, User.name)\
        .order_by(func.sum(Order.total_amount).desc())\
        .limit(10)\
        .all()

def get_highest_sold_products():
    """Get report of best selling products"""
    session = get_sqlalchemy_session()
    return (
        session.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label("total_quantity"),
        )
        .select_from(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(Product, Product.id == OrderItem.product_id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
        .all()
    )