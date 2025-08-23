from flask import Flask, jsonify, request
from model.usagerecord import UsageRecord
from model.data import data
app = Flask(__name__)

@app.route('/')
def hello_world():
    customer_names_array = ['Alice', 'Bob', 'Charlie']
    return jsonify(customer_names_array)  # Return JSON response
@app.route('/dat')
def hh():
    usage_record = UsageRecord("U001", "C001", "SMS", 1, "2025-08-22", 0, "Bob", 0.10, "Completed")
    return jsonify(usage_record.__dict__)  # assuming UsageRecord is a regular class

@app.route('/create', methods=["post"])
def create():
    data:{
            "name" : self.name,
            "age" : self.age,
            "birth" : self.birth
        }
    


if __name__ == "__main__":
    app.run(debug=True)
