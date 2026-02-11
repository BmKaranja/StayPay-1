from app.extensions import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)

    # Links: Who is paying whom?
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)

    # Transaction Details
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)  # Unique (ffrom paystack)Receipt
    description = db.Column(db.Text)

    # Payment Status
    status = db.Column(db.String(20), default='Pending')

    payment_method = db.Column(db.String(50), default='M-Pesa')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Automatically updates whenever you change the status
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_reference(cls, reference):
        """Find a payment by its unique Paystack reference"""
        return cls.query.filter_by(reference=reference).first()