from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.models.tenant_model import Tenant
from app import db
from app.models.landlord_model import Landlord

@jwt_required()   #(security)Only allows requests with a valid Token
def add_tenant_logic():
    current_landlord_id = get_jwt_identity() # Extract id from the token
    data = request.get_json()

    # Validation
    required = ['name', 'phone_no', 'house_no', 'rent_payable']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Check if House Number is already taken (for this landlord)
    if Tenant.check_availability(data['house_no'], current_landlord_id):
        return jsonify({"error": f"House {data['house_no']} is already occupied"}), 409

    # Create Tenant (With Default Password):Tenant123
    default_password = generate_password_hash("Tenant123")

    new_tenant = Tenant(
        landlord_id=current_landlord_id,
        name=data['name'],
        phone_no=data['phone_no'],
        house_no=data['house_no'],
        password=default_password,
        rent_due=float(data['rent_payable']), # Set how much they should pay
        rent_status='Unpaid',
        balance=0.0
    )

    # Save
    try:
        new_tenant.save()
        return jsonify({
            "message": "Tenant added successfully!",
            "details": {
                "username": data['house_no'],
                "default_password": "Tenant123"
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Tenant LOGIN LOGIC
def login_tenant_logic():
    data = request.get_json()

    # Login using House Number(as username)
    house_no = data.get('house_no')
    password = data.get('password')

    if not house_no or not password:
        return jsonify({"error": "Missing House Number or Password"}), 400

    # Find Tenant
    tenant = Tenant.get_by_house(house_no)

    # Verify Password
    if tenant and check_password_hash(tenant.password, password):
        # Create Token for Tenant
        access_token = create_access_token(identity=str(tenant.id))

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "house_no": tenant.house_no,
                "rent_status": tenant.rent_status,
                "balance": tenant.balance
            }
        }), 200

    return jsonify({"error": "Invalid House Number or Password"}), 401


#chaanging PASSWORD LOGIC (Tenant Only)
@jwt_required()
def change_password_logic():
    current_tenant_id = get_jwt_identity()  #Get Tenant ID from Token
    data = request.get_json()

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"error": "Both old and new passwords are required"}), 400

    # Get Tenant from DB
    tenant = Tenant.query.get(current_tenant_id)

    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    # Verify Old Password
    if not check_password_hash(tenant.password, old_password):
        return jsonify({"error": "Incorrect old password"}), 401

    # Save New Password
    tenant.password = generate_password_hash(new_password)

    try:
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#DASHBOARD stats logic
@jwt_required()
def get_dashboard_stats_logic():
    current_landlord_id = get_jwt_identity()

    # Get Landlord Details (to know total houses)
    landlord = Landlord.query.get(current_landlord_id)
    if not landlord:
        return jsonify({"error": "Landlord not found"}), 404

    # Get Counts using our Model helpers
    occupied = Tenant.count_occupied(current_landlord_id)
    paid = Tenant.count_paid(current_landlord_id)
    unpaid = Tenant.count_unpaid(current_landlord_id)

    # Calculate Vacant
    total_houses = landlord.total_houses
    vacant = total_houses - occupied

    return jsonify({
        "stats": {
            "total_houses": total_houses,
            "occupied": occupied,
            "vacant": vacant,
            "paid": paid,
            "unpaid": unpaid
        }
    }), 200


# GET ALL TENANTS LOGIC (For the Table)
@jwt_required()
def get_all_tenants_logic():
    current_landlord_id = get_jwt_identity()

    # Fetch from DB
    tenants = Tenant.get_all_by_landlord(current_landlord_id)

    # Convert list of objects to JSON
    output = []
    for tenant in tenants:
        output.append({
            "id": tenant.id,
            "name": tenant.name,
            "house_no": tenant.house_no,
            "phone_no": tenant.phone_no,
            "rent_status": tenant.rent_status,
            "rent_due": tenant.rent_due,
            "balance": tenant.balance
        })

    return jsonify({"tenants": output}), 200