from urllib import response
from flask import Flask, jsonify, request
from models.customer import Customer

app = Flask(__name__)
customers = []

# Health check endpoint 
@app.route('/ping')
def test_app():             
    return "app is running"

# Retrieve customer information
@app.route('/customer', methods=['GET'])
def get_customer_info():
    # customer = Customer(1, "John Doe", 30, "123 Main St", "Jane Doe", "2023-01-01",'Male',"john.doe@example.com")
    return jsonify(customers), 200



# Create a new customer
@app.route('/create', methods=['POST'])
def create_customer():
    data = request.get_json()
    print(data)


    customer = {
        'customer_id': data.get('Id'),
        'name': data.get('Name'),
        'age': data.get('Age'),
        'address': data.get('Address'),
        'mother_name': data.get('MotherName'),
        'date_of_registration': data.get('DateOfRegistration'),
        'gender': data.get('Gender'),
        'email': data.get('Email')
    }



    customers.append(customer)
    return jsonify(customers), 201


if __name__ == '__main__':
    app.run()

