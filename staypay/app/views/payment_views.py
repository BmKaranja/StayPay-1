import uuid
import requests
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.payment_model import Payment
from app.models.tenant_model import Tenant
from app.extensions import db


# INITIATE PAYMENT
@jwt_required()
def initiate_payment_logic():
    current_tenant_id = get_jwt_identity()
    data = request.get_json()

    amount = data.get('amount')
    phone_no = data.get('phone_no')

    if not amount or not phone_no:
        return jsonify({"error": "Missing amount or phone number"}), 400

    tenant = Tenant.query.get(current_tenant_id)
    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    # Generate unique reference
    reference = f"PAY-{uuid.uuid4().hex[:8].upper()}"

    # Save Pending Transaction
    new_payment = Payment(
        tenant_id=tenant.id,
        landlord_id=tenant.landlord_id,
        amount=float(amount),
        reference=reference,
        description=f"Rent Payment by {tenant.name}",
        status='Pending',
        payment_method='Paystack/M-Pesa'
    )

    try:
        new_payment.save()
    except Exception as e:
        return jsonify({"error": f"Database Error: {str(e)}"}), 500

    # Talk to Paystack
    paystack_url = "https://api.paystack.co/transaction/initialize"
    secret_key = current_app.config['PAYSTACK_SECRET_KEY']

    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "email": f"{tenant.house_no}@staypay.com",
        "amount": int(float(amount) * 100),  # Convert to cents/kobo
        "currency": "KES",
        "reference": reference,
        "callback_url": "http://127.0.0.1:5000/api/payment/callback",
        "metadata": {
            "tenant_id": tenant.id,
            "custom_fields": [{"display_name": "Phone", "variable_name": "phone", "value": phone_no}]
        }
    }

    try:
        response = requests.post(paystack_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return jsonify({
                "message": "Payment initiated successfully",
                "authorization_url": response_data['data']['authorization_url'],
                "reference": reference
            }), 200
        else:
            return jsonify({"error": "Paystack Error", "details": response_data}), 400

    except Exception as e:
        return jsonify({
            "message": "Payment recorded locally (Connection Failed)",
            "reference": reference,
            "status": "Pending",
            "error": str(e)
        }), 201


# VERIFY PAYMENT
@jwt_required()
def verify_payment_logic(reference):
    """
    1. Tenant clicks "I have Paid".
    2. We ask Paystack: "Is this reference paid?"
    3. If yes, we update the database and the tenant's rent balance.
    """
    # Find the local transaction
    payment = Payment.get_by_reference(reference)

    if not payment:
        return jsonify({"error": "Payment reference not found"}), 404

    if payment.status == 'Success':
        return jsonify({"message": "Payment already verified"}), 200

    # Ask Paystack (REAL VERIFICATION)
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
    }

    try:
        # Call Paystack
        response = requests.get(verify_url, headers=headers)
        response_data = response.json()

        # Check if Paystack says "success"
        if response_data['status'] is True and response_data['data']['status'] == 'success':

            # UPDATE PAYMENT STATUS
            payment.status = 'Success'
            payment.save()

            # UPDATE TENANT BALANCE
            tenant = Tenant.query.get(payment.tenant_id)

            # Deduct the amount paid from their balance
            tenant.balance = tenant.balance - payment.amount

            # Update Rent Status
            if tenant.balance <= 0:
                tenant.rent_status = 'Paid'
                # Optional: Handle overpayment (negative balance means credit)
            else:
                tenant.rent_status = 'Unpaid'

            tenant.save()  # Save the new balance

            return jsonify({
                "message": "Payment Verified & Balance Updated!",
                "new_balance": tenant.balance,
                "rent_status": tenant.rent_status
            }), 200

        else:
            return jsonify({
                "message": "Payment Verification Failed",
                "paystack_status": response_data['data']['status']
            }), 400

    except Exception as e:
        return jsonify({"error": "Connection to Paystack failed", "details": str(e)}), 500