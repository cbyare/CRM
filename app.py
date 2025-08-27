from urllib import response
from flask import Flask, jsonify, request
from models.customer import Customer
from models.transactions import Transaction
from api.smsapi import send_sms
from ussd.ussd import get_menu


app = Flask(__name__)
customers = []
transactions = []

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

# Get all transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify([t.to_dict() for t in transactions]), 200

# Create new transaction
@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    print(data)

    transaction = Transaction(
        transaction_id=data.get('Id'),
        service_id=data.get('ServiceId'),
        customer_id=data.get('CustomerId'),
        amount=data.get('Amount'),
        transaction_type=data.get('TransactionType'),
        action_user=data.get('ActionUser'),
        status=data.get('Status'),
        date=data.get('Date')
    )

    transactions.append(transaction)

    message = {
        'status': 'success',
        'message': 'Transaction created successfully',
        'code': 201
    }
    return jsonify(transaction.to_dict()), 201

if __name__ == '__main__':
    app.run()

