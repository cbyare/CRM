import os
from flask import Flask, jsonify, request, send_file
from configs.db import db, init_db
from models.customer import Customer
from ussd.ussd import get_menu
from api.smsapi import send_sms
from reports import total_customers, list_customer_names, generate_pdf_report  # new import

app = Flask(__name__)

# Database config from environment variables
app.config['DB_USER'] = os.environ.get('DB_USER', 'postgres')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'Iidle44')
app.config['DB_HOST'] = os.environ.get('DB_HOST', 'postgres')
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
# Customer Endpoints (POST, GET, PUT, DELETE)
# -------------------------
# (Keep all existing customer routes unchanged)

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
# Reporting Endpoints
# -------------------------
@app.route('/reports/customers', methods=['GET'])
def customer_report():
    """Return JSON report of customers."""
    customers = Customer.query.all()
    report = {
        'total_customers': total_customers(customers),
        'customer_names': list_customer_names(customers)
    }
    return jsonify(report), 200

@app.route('/reports/customers/pdf', methods=['GET'])
def customer_report_pdf():
    """Generate and return PDF report of customers."""
    customers = Customer.query.all()
    filename = generate_pdf_report(customers)
    return send_file(filename, as_attachment=True)

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database connected and tables created successfully!")
    app.run(host='0.0.0.0', port=5000)
