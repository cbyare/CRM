from urllib import response
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

from models.customer import Customer
from api.smsapi import send_sms
from ussd.ussd import get_menu


# Load environment variables
load_dotenv()

app = Flask(__name__)
# Database config
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------
# MODELS
# -------------------------
class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)  # Just integers
    service_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    plan_type = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "service_id": self.service_id,
            "status": self.status,
            "plan_type": self.plan_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

customers = []

# Health check endpoint 
@app.route('/ping')
def test_app(): 

    message = {
        'status': 'success',
        'message': 'app is running',
        'code': 200
    } 

    return jsonify(message)

@app.route("/create-subscription", methods=["POST"])
def create_subscription():
    data = request.get_json()
    try:
        subscription = Subscription(
            customer_id=data.get("customer_id", 1),
            service_id=data.get("service_id", 1),
            status=data.get("status", "active"),
            plan_type=data.get("plan_type", "basic"),
        )

        db.session.add(subscription)
        db.session.commit()

        return jsonify(subscription.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    subs = Subscription.query.all()
    return jsonify([s.to_dict() for s in subs])

# Retrieve customer information
@app.route('/customer', methods=['GET'])
def get_customer_info():
    print(request.headers)

    # customer = Customer(1, "John Doe", 30, "123 Main St", "Jane Doe", "2023-01-01",'Male',"john.doe@example.com")
    return jsonify(customers), 200



# Create a new customer
@app.route('/create', methods=['POST'])
def create_customer():
    data = request.get_json()
    print(request.headers)

    print(data)


    customer = {
        'customer_id': data.get('Id'),
        'name': data.get('Name'),
        'phone_number': data.get('Phone'),
        'age': data.get('Age'),
        'address': data.get('Address'),
        'mother_name': data.get('MotherName'),
        'date_of_registration': data.get('DateOfRegistration'),
        'gender': data.get('Gender'),
        'email': data.get('Email')
    }

    customers.append(customer)

     # API CALL TO SEND SMS FOR THE NEW CUSTOMER REGISTRATION
    response = send_sms(data.get('Phone'), f"Welcome {data.get('Name')}! You have been registered successfully.", "Istaqaana")
    print(response.get('ResponseCode'))
    print(response['ResponseCode'])


    if response.get('ResponseCode') == '200':
        message = {
            'status': 'success',
            'message': 'Customer created and SMS sent successfully',
            'code': 201
        }
    else:
        message = {
            'status': 'error',
            'message': 'Customer created but failed to send SMS',
            'code': 500
        }
    return jsonify(customer), message['code'], message


@app.route('/ussd', methods=['POST'])
def get_menu_endpoint():
    data = request.get_json()
    ussd_string = data.get('ussdcontent')
    print(ussd_string)


    menu = get_menu(ussd_string)


    requestid = data.get('requestid', '')
    origin = data.get('mobile', '')
    sessionid = data.get('dailogid', '')
    end_reply = data.get('end_reply', '')
    ussdstate = data.get('ussd_state', '')
    shortcode = data.get('shortcode', '')
     
    res = {
        'requestid': requestid,
        'origin': origin,
        'sessionid': sessionid,
        'ussdstate': 'continue',
        'shortcode': shortcode,
        'message': menu,
        'endreply': 'false',
    }

    return jsonify(res), 200


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        print("✅ Database connected and tables created successfully!")
    except Exception as e:
        print("❌ Database connection failed:", e)
    app.run()

