from flask import Blueprint
from app.views.landlord_views import register_landlord_logic, login_landlord_logic
from app.views.tenant_views import get_dashboard_stats_logic, get_all_tenants_logic

landlord_bp = Blueprint('landlord', __name__)

@landlord_bp.route('/register', methods=['POST'])
def register():
    return register_landlord_logic()

@landlord_bp.route('/login', methods=['POST'])
def login():
    return login_landlord_logic()

@landlord_bp.route('/dashboard-stats', methods=['GET'])
def get_stats():
    return get_dashboard_stats_logic()

@landlord_bp.route('/tenants', methods=['GET'])
def get_tenants():
    return get_all_tenants_logic()