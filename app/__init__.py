from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_migrate import Migrate
from .config import Configuration
from .models import db, Customer, Flight
from .auth import AuthError, requires_auth
from .calculate_trip import calculate_trip


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    Migrate(app, db)

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.route("/calculate-trip", methods=["POST"])
    def calculate():
        req = request.get_json()
        depart = req['depart']
        arrive = req['arrive']
        date = req['date']
        distance = calculate_trip(depart, arrive, date)
        return {'distance': distance.value}

    @app.route("/users", methods=["POST"])
    @requires_auth
    def update_user():
        body = request.get_json()
        # checks if there there is user in db
        db_user = Customer.query.filter_by(email=body['email']).first()
        if db_user:  # if user exists updates the user's name
            db_user.name = body['name']
            return jsonify({'userId': db_user.id}), 201
        else:  # no user exists create a new user
            new_user = Customer(name=body['name'],
                                email=body['email'],
                                auth0_id=body['auth0_id'],
                                picture=body['picture'])
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'userId': new_user.id}), 201

    @app.route("/flights/<int:id>")
    @requires_auth
    def get_flights(id):
        flights_for_user = Flight.query.filter(Flight.customer_id == id).all()
        flights = [flight.to_dict() for flight in flights_for_user]
        return jsonify(flights)

    @app.route("/flights", methods=["POST"])
    @requires_auth
    def create_flight():
        body = request.get_json()
        new_flight = Flight(customer_id=body['customer_id'],
                            depart_date=body['depart_date'],
                            depart_loc=body['depart_loc'],
                            arrive_loc=body['arrive_loc'],
                            num_pass=body['num_pass'],
                            ticket_price=body['ticket_price'],
                            ticket_class=body['ticket_class'],
                            distance=body['distance'],
                            travel_time=body['travel_time'])
        db.session.add(new_flight)
        db.session.commit()

        return 'Flight created', 201

    return app