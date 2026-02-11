from app.extensions import db
from datetime import datetime


class Landlord(db.Model):
    __tablename__ = 'landlords'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20))

    # Apartment Info
    apartment_name = db.Column(db.String(100))
    caretaker_name = db.Column(db.String(100))
    default_rent_amount = db.Column(db.Float, default=0.0)
    total_houses = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Helper to save this object to DB"""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        """Helper to find user by email"""
        return cls.query.filter_by(email=email).first()