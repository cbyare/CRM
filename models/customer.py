from configs.db import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    mother_name = db.Column(db.String(100))
    date_of_registration = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'age': self.age,
            'address': self.address,
            'mother_name': self.mother_name,
            'date_of_registration': self.date_of_registration,
            'gender': self.gender,
            'email': self.email
        }
