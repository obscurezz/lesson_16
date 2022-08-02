import sqlalchemy.exc

from flask import Blueprint, jsonify, request

from models import db, Order

orders_blueprint = Blueprint('orders', __name__)


@orders_blueprint.route('/orders', methods=['GET', 'PUT'])
def select_all_orders():
    # post method/insert
    if request.method == 'POST':
        req: dict = request.get_json()
        new_order: Order = Order(**req)
        db.session.add(new_order)
        try:
            db.session.commit()
            return jsonify(new_order._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                       'message': 'Integrity Error',
                       'error': str(e),
                       'status_code': 500
                   }, 500
    # get method/select
    else:
        query = [o._as_dict() for o in Order.query.all()]
        return jsonify(query), 200


@orders_blueprint.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def select_order_by_pk(pk: int):
    order: Order = Order.query.get(pk)
    # put method/update
    if request.method == 'PUT':
        req: dict = request.get_json()
        for k in req:
            setattr(order, k, req[k])
        try:
            db.session.commit()
            return jsonify(order._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                       'message': 'Integrity Error',
                       'error': str(e),
                       'status_code': 500
                   }, 500
    # delete method/delete
    elif request.method == 'DELETE':
        db.session.delete(order)
        try:
            db.session.commit()
            return {
                'message': 'Deleted user',
                'user': order._as_dict()
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                       'message': 'Integrity Error',
                       'error': str(e),
                       'status_code': 500
                   }, 500
    # get method/select
    else:
        return jsonify(order._as_dict()), 200
