import sqlalchemy.exc

from flask import Blueprint, jsonify, request

from models import db, Offer

offers_blueprint = Blueprint('offers', __name__)


@offers_blueprint.route('/offers', methods=['GET', 'POST'])
def select_all_offers():
    # post method/insert
    if request.method == 'POST':
        req: dict = request.get_json()
        new_offer: Offer = Offer(**req)
        db.session.add(new_offer)
        try:
            db.session.commit()
            return jsonify(new_offer._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                       'message': 'Integrity Error',
                       'error': str(e),
                       'status_code': 500
                   }, 500
    # get method/select
    else:
        query = [o._as_dict() for o in Offer.query.all()]
        return jsonify(query), 200


@offers_blueprint.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def select_offer_by_pk(pk: int):
    offer: Offer = Offer.query.get(pk)
    # put method/update
    if request.method == 'PUT':
        req: dict = request.get_json()
        for k in req:
            setattr(offer, k, req[k])
        try:
            db.session.commit()
            return jsonify(offer._as_dict()), 200
        except sqlalchemy.exc.IntegrityError as e:
            return {
                    'message': 'Integrity Error',
                    'error': str(e),
                    'status_code': 500
                    }, 500
    # delete method/delete
    elif request.method == 'DELETE':
        db.session.delete(offer)
        try:
            db.session.commit()
            return {
                'message': 'Deleted user',
                'user': offer._as_dict()
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                    'message': 'Integrity Error',
                    'error': str(e),
                    'status_code': 500
                    }, 500
    # get method/select
    else:
        return jsonify(offer._as_dict()), 200
