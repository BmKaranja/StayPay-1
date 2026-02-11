from app.extensions import db
from datetime import datetime


class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    # Link to the Landlord table
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    house_no = db.Column(db.String(20), nullable=False)  # Acts as Username
    password = db.Column(db.String(255), nullable=False)

    #Financials
    rent_status = db.Column(db.Enum('Paid', 'Unpaid'), default='Unpaid')
    rent_due = db.Column(db.Float, default=0.00)
    balance = db.Column(db.Float, default=0.00)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    #Used when ADDING a tenant.
    #Checks if a specific house is already taken within this landlord's apartment
    @classmethod
    def check_availability(cls, house_no, landlord_id):
        """Check if a house is already taken in this specific apartment"""
        return cls.query.filter_by(house_no=house_no, landlord_id=landlord_id).first()

    #helper function used for TENANT LOGIN to help find the tenat by house number(username)
    @classmethod
    def get_by_house(cls, house_no):
        """Find a tenant strictly by their House Number (Username)"""
        return cls.query.filter_by(house_no=house_no).first()

    #helper function to get all tenants(for a unique landlord)
    @classmethod
    def get_all_by_landlord(cls, landlord_id):
        """Fetch all tenants belonging to a specific landlord"""
        return cls.query.filter_by(landlord_id=landlord_id).all()


    @classmethod
    def count_occupied(cls, landlord_id):
        """Count how many houses are occupied"""
        return cls.query.filter_by(landlord_id=landlord_id).count()


    @classmethod
    def count_paid(cls, landlord_id):
        """Count how many tenants have status 'Paid'"""
        return cls.query.filter_by(landlord_id=landlord_id, rent_status='Paid').count()


    @classmethod
    def count_unpaid(cls, landlord_id):
        """Count how many tenants have status 'Unpaid'"""
        return cls.query.filter_by(landlord_id=landlord_id, rent_status='Unpaid').count()