import sqlalchemy.exc

from flask import Blueprint, jsonify, request

from models import db, Order

orders_blueprint = Blueprint('orders', __name__)


@orders_blueprint.route('/orders', methods=['GET', 'PUT'])
def select_all_orders():
    if request.method == 'POST':
        req = request.get_json()
        new_order = Order(**req)
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

    else:
        query = [o._as_dict() for o in Order.query.all()]
        return jsonify(query), 200


@orders_blueprint.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def select_order_by_pk(pk: int):
    order = Order.query.get(pk)

    if request.method == 'PUT':
        req = request.get_json()
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

    else:
        return jsonify(order._as_dict()), 200
