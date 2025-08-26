from flask import Flask, jsonify, request
from models.UsageRecord import UsageRecords
from api.sms import sms

app = Flask(__name__)

usage_records = []

@app.route('/Track', methods=['POST'])
def New_Usage():
    data = request.get_json()
    print(data)

    usage_record = UsageRecords.from_dict(data)
    usage_records.append(usage_record)

    response = sms(data.get('Phone'), f"Welcome {data.get('Name')}! You have been registered successfully.", "Istaqaana")
    print(response.get('ResponseCode'))
    print(response['ResponseCode'])

    return jsonify(usage_record.to_dict()), 201

@app.route('/Tracked', methods=['GET'])
def get_Usage():
    return jsonify([record.to_dict() for record in usage_records]), 200


# DELETE all usage records
@app.route('/Tracked', methods=['DELETE'])
def delete_all_usage():
    usage_records.clear()
    return jsonify({"message": "All usage records have been deleted"}), 200


# DELETE a specific usage record (by ID)
@app.route('/Tracked/<usage_id>', methods=['DELETE'])
def delete_usage(usage_id):
    global usage_records
    for record in usage_records:
        if record.Usage_id == usage_id:   # ✅ match your JSON field
            usage_records.remove(record)
            return jsonify({"message": f"Usage record {usage_id} deleted"}), 200
    return jsonify({"error": "Record not found"}), 404




if __name__ == "__main__":
    app.run(debug=True)
