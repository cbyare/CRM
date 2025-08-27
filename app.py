from flask import Flask, jsonify, request
from datetime import datetime
from database import app, db, Customer, Services

# Health check
@app.route('/ping')
def ping():
    return "App is running", 200


# -------- CUSTOMER ENDPOINTS ---------

# Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    result = []
    for c in customers:
        result.append({
            'Id': c.Id,
            'Name': c.Name,
            'Age': c.Age,
            'Address': c.Address,
            'MotherName': c.MotherName,
            'DateOfRegistration': c.DateOfRegistration.isoformat() if c.DateOfRegistration else None,
            'Gender': c.Gender,
            'Email': c.Email
        })
    return jsonify(result), 200

# Create a new customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        Name=data.get('Name'),
        Age=data.get('Age'),
        Address=data.get('Address'),
        MotherName=data.get('MotherName'),
        DateOfRegistration=datetime.fromisoformat(data['DateOfRegistration']) if 'DateOfRegistration' in data else None,
        Gender=data.get('Gender'),
        Email=data.get('Email')
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201


# -------- SERVICES ENDPOINTS ---------

# Get all services
@app.route('/services', methods=['GET'])
def get_services():
    services = Services.query.all()
    result = []
    for s in services:
        result.append({
            'ServiceId': s.ServiceId,
            'ServiceName': s.ServiceName,
            'Description': s.Description,
            'ServiceTime': s.ServiceTime.isoformat() if s.ServiceTime else None
        })
    return jsonify(result), 200

# Create a new service
@app.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    new_service = Services(
        ServiceName=data.get('ServiceName'),
        Description=data.get('Description'),
        ServiceTime=datetime.fromisoformat(data['ServiceTime']) if 'ServiceTime' in data else None
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
