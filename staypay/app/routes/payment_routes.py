from flask import Blueprint
from app.views.payment_views import initiate_payment_logic, verify_payment_logic

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/initiate', methods=['POST'])
def initiate_payment():
    return initiate_payment_logic()

@payment_bp.route('/verify/<reference>', methods=['GET'])
def verify_payment(reference):
    return verify_payment_logic(reference)