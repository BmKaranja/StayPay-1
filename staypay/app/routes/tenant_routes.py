from flask import Blueprint
from app.views.tenant_views import add_tenant_logic, login_tenant_logic, change_password_logic

# Define Blueprint
tenant_bp = Blueprint('tenant', __name__)

# Route to Add Tenant (Requires Landlord Token)
@tenant_bp.route('/add', methods=['POST'])
def add_tenant():
    return add_tenant_logic()

# Route to Login as Tenant(Public - Uses House No as username)
@tenant_bp.route('/login', methods=['POST'])
def login():
    return login_tenant_logic()

# Route to Change Password (Requires Tenant Token)
@tenant_bp.route('/change-password', methods=['PUT'])
def change_password():
    return change_password_logic()