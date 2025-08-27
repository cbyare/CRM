from flask import Flask
from models import db

# Models hadda jira
from models.customer import Customer
from models.service import Services

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/tt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Table-yadii hadda la heli karo waa la abuuray.")
