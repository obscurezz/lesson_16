import sqlalchemy.exc

from flask import Blueprint, jsonify, request

from models import db, User

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users', methods=['GET', 'POST'])
def select_all_users():
    if request.method == 'POST':
        req = request.get_json()
        new_user = User(**req)
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify(new_user._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                    'message': 'Integrity Error',
                    'error': str(e),
                    'status_code': 500
                    }, 500

    else:
        query = [u._as_dict() for u in User.query.all()]
        return jsonify(query), 200


@users_blueprint.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def select_user_by_pk(pk: int):
    user = User.query.get(pk)

    if request.method == 'PUT':
        req = request.get_json()
        for k in req:
            setattr(user, k, req[k])
        try:
            db.session.commit()
            return jsonify(user._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                    'message': 'Integrity Error',
                    'error': str(e),
                    'status_code': 500
                    }, 500

    elif request.method == 'DELETE':
        db.session.delete(user)
        try:
            db.session.commit()
            return {
                'message': 'Deleted user',
                'user': user._as_dict()
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                    'message': 'Integrity Error',
                    'error': str(e),
                    'status_code': 500
                    }, 500

    else:
        return jsonify(user._as_dict()), 200