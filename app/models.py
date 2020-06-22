from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
          'customers.id'), nullable=False)
    depart_date = db.Column(db.String(50), nullable=False)
    depart_loc = db.Column(db.String(25), nullable=False)
    arrive_loc = db.Column(db.String(25), nullable=False)
    num_pass = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    ticket_class = db.Column(db.String(25), nullable=False)
    distance = db.Column(db.String(25), nullable=False)
    travel_time = db.Column(db.Integer, nullable=False)

    customer = db.relationship('Customer', back_populates='flights')


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    auth0_id = db.Column(db.String, unique=True)
    picture = db.Column(db.String)

    flights = db.relationship('Flight', back_populates='customer')