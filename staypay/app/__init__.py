from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from app.extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Initialize Extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    #loading tables first so they are visible
    from app.models.landlord_model import Landlord
    from app.models.tenant_model import Tenant
    from app.models.payment_model import Payment

    # Setup Migrations (Handles database table creation updates)
    Migrate(app, db)

    # 2. Register Blueprints
    from app.routes.landlord_routes import landlord_bp
    from app.routes.tenant_routes import tenant_bp
    from app.routes.payment_routes import payment_bp

    app.register_blueprint(landlord_bp, url_prefix='/api/landlord')
    app.register_blueprint(tenant_bp, url_prefix='/api/tenant')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')


    # 3. Create Tables (Quick setup for development)
    with app.app_context():
        db.create_all()

    return app