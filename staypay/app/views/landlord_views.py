from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.landlord_model import Landlord
from flask_jwt_extended import create_access_token

def register_landlord_logic():
    data = request.get_json()

    # Validation
    required = ['name', 'email', 'password', 'apartment_name']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Checking if email exists
    if Landlord.get_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 409

    # Create the Object
    new_landlord = Landlord(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        phone_no=data.get('phone_no'),
        apartment_name=data['apartment_name'],
        caretaker_name=data.get('caretaker_name'),
        default_rent_amount=data.get('rent_amount', 0),
        total_houses=data.get('total_houses', 0)
    )

    # Save to DB (Using ORM helper)
    try:
        new_landlord.save()
        return jsonify({"message": "Landlord registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Landlord login logic
def login_landlord_logic():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    #validation
    if not email or not password:
        return jsonify({"Error": "Email and Password are required"}), 400

    #finding the landlord(using the model)
    landlord = Landlord.get_by_email(email)

    #verifying password
    if landlord and check_password_hash(landlord.password, password):
        #creating an access token for the landlord signing in
        access_token = create_access_token(identity=str(landlord.id))

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "landlord": {
                "id": landlord.id,
                "name": landlord.name,
                "apartment": landlord.apartment_name
            }
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401