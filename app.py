from flask import Flask, jsonify, request
from datetime import datetime

from models.customer import Customer
from api.smsapi import send_sms
from ussd.ussd import get_menu

# 🔹 NEW: import db from configs
from configs.db import db, init_db


app = Flask(__name__)

# 🔹 NEW: Initialize DB connection
init_db(app)


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


# -------------------------
# SUBSCRIPTION ENDPOINTS
# -------------------------

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


# 🔹 NEW: Get subscription by ID
@app.route("/subscriptions/<int:sub_id>", methods=["GET"])
def get_subscription(sub_id):
    sub = Subscription.query.get(sub_id)
    if not sub:
        return jsonify({"error": "Subscription not found"}), 404
    return jsonify(sub.to_dict()), 200


# 🔹 NEW: Delete subscription by ID
@app.route("/subscriptions/<int:sub_id>", methods=["DELETE"])
def delete_subscription(sub_id):
    sub = Subscription.query.get(sub_id)
    if not sub:
        return jsonify({"error": "Subscription not found"}), 404

    db.session.delete(sub)
    db.session.commit()
    return jsonify({"message": f"Subscription {sub_id} deleted"}), 200


# -------------------------
# EXISTING CUSTOMER + USSD ROUTES (UNCHANGED)
# -------------------------
@app.route('/customer', methods=['GET'])
def get_customer_info():
    print(request.headers)
    return jsonify(customers), 200


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

    response = send_sms(data.get('Phone'), f"Welcome {data.get('Name')}! You have been registered successfully.", "Istaqaana")

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

    res = {
        'requestid': data.get('requestid', ''),
        'origin': data.get('mobile', ''),
        'sessionid': data.get('dailogid', ''),
        'ussdstate': 'continue',
        'shortcode': data.get('shortcode', ''),
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
