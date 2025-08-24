from urllib import response
from flask import Flask, jsonify, request
from models.customer import Customer
from api.smsapi import send_sms


app = Flask(__name__)
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


if __name__ == '__main__':
    app.run()

