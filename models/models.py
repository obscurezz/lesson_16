from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    def _as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(50), nullable=False)
    last_name = db.Column(db.VARCHAR(50), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    role = db.Column(db.VARCHAR(20), db.CheckConstraint("role IN ('executor', 'customer')"), nullable=False)
    phone = db.Column(db.VARCHAR(30), unique=True)


class Offer(db.Model):

    def _as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Order(db.Model):

    def _as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    description = db.Column(db.VARCHAR(200))
    start_date = db.Column(db.VARCHAR(20))
    end_date = db.Column(db.VARCHAR(20))
    address = db.Column(db.VARCHAR(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("offer.executor_id"))
