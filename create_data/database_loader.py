import json
import sqlalchemy.exc
from os import path

from models import db


def create_data_for_table(jsonfile: path, model: db.Model):
    with open(jsonfile, 'r', encoding='utf-8') as file:
        loading_data: list[dict] = json.load(file)

        for item in loading_data:
            db.session.add(model(**item))

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print({'INFO': e})
