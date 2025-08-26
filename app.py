import os
from flask import Flask, jsonify, request
from configs.db import db, init_db
from models.customer import Customer
from ussd.ussd import get_menu
from api.smsapi import send_sms

app = Flask(__name__)

# Database config from environment variables
app.config['DB_USER'] = os.environ.get('DB_USER', 'postgres')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'Iidle44')
app.config['DB_HOST'] = os.environ.get('DB_HOST', 'postgres')  # Docker service
app.config['DB_PORT'] = os.environ.get('DB_PORT', '5432')
app.config['DB_NAME'] = os.environ.get('DB_NAME', 'crm_db')

init_db(app)

# -------------------------
# Health Check
# -------------------------
@app.route('/ping')
def test_app():
    return jsonify({'status': 'success', 'message': 'app is running', 'code': 200})

# -------------------------
# Customer Endpoints
# -------------------------
@app.route('/customers', methods=['POST'])
def create_or_update_customer():
    data = request.get_json()
    try:
        customer = Customer.query.filter(
            (Customer.email == data.get('Email')) |
            (Customer.phone_number == data.get('Phone'))
        ).first()

        if customer:
            for key, val in {
                'name': data.get('Name'),
                'phone_number': data.get('Phone'),
                'age': data.get('Age'),
                'address': data.get('Address'),
                'mother_name': data.get('MotherName'),
                'date_of_registration': data.get('DateOfRegistration'),
                'gender': data.get('Gender'),
                'email': data.get('Email')
            }.items():
                if val:
                    setattr(customer, key, val)
            db.session.commit()
            return jsonify(customer.to_dict()), 200

        customer = Customer(
            name=data.get('Name'),
            phone_number=data.get('Phone'),
            age=data.get('Age'),
            address=data.get('Address'),
            mother_name=data.get('MotherName'),
            date_of_registration=data.get('DateOfRegistration'),
            gender=data.get('Gender'),
            email=data.get('Email')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify([c.to_dict() for c in Customer.query.all()]), 200

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict()), 200

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    for key in ['name', 'phone_number', 'age', 'address', 'mother_name', 'gender', 'email']:
        if data.get(key.capitalize()):
            setattr(customer, key, data.get(key.capitalize()))

    db.session.commit()
    return jsonify(customer.to_dict()), 200

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted'}), 200

# -------------------------
# USSD Endpoint
# -------------------------
@app.route('/ussd', methods=['POST'])
def get_menu_endpoint():
    data = request.get_json()
    menu = get_menu(data.get('ussdcontent'))
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

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database connected and tables created successfully!")
    app.run(host='0.0.0.0', port=5000)
