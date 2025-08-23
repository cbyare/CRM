from flask import Flask, jsonify, request
from models.UsageRecord import UsageRecords

app = Flask(__name__)

usage_records = []

@app.route('/Track', methods=['POST'])
def New_Usage():
    data = request.get_json()
    print(data)

    usage_record = UsageRecords.from_dict(data)
    usage_records.append(usage_record)

    return jsonify(usage_record.to_dict()), 201

@app.route('/Tracked', methods=['GET'])
def get_Usage():
    return jsonify([record.to_dict() for record in usage_records]), 200

if __name__ == "__main__":
    app.run(debug=True)
