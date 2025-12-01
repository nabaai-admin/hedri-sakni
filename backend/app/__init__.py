from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger
import logging
import os

from app.config import config
from app.models import db
from app.services.scheduler import reservation_scheduler
from app.utils.auth import generate_token

# Import blueprints
from app.routes.areas import areas_bp
from app.routes.customers import customers_bp
from app.routes.reservations import reservations_bp
from app.routes.analytics import analytics_bp
from app.routes.external import external_bp

migrate = Migrate()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Land Reservation Admin API",
            "description": "API for managing land reservation attempts with UiPath integration",
            "version": "1.0.0",
            "contact": {
                "name": "API Support"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        "definitions": {
            "Area": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "is_active": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "Customer": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "description": "الاسم"},
                    "phone_number": {"type": "string", "description": "رقم الهاتف"},
                    "national_id": {"type": "string", "description": "الرقم الوطني"},
                    "area_id": {"type": "integer", "description": "المنطقة"},
                    "area_name": {"type": "string"},
                    "reservation_status": {"type": "string", "enum": ["OPEN", "SUCCESS", "FAILED"], "description": "حالة الحجز"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    app.register_blueprint(areas_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(external_bp)
    
    # Register auth routes
    register_auth_routes(app)
    
    # Initialize scheduler
    reservation_scheduler.init_app(app)
    
    # Reschedule pending slots on startup
    with app.app_context():
        reservation_scheduler.reschedule_all_pending_slots()
    
    # Error handlers
    register_error_handlers(app)
    
    return app


def setup_logging(app):
    """Configure application logging"""
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(app.config['LOG_FILE']),
            logging.StreamHandler()
        ]
    )
    
    app.logger.setLevel(log_level)


def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """
        Admin login endpoint
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Login successful
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                token:
                  type: string
          401:
            description: Invalid credentials
        """
        data = request.json
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        username = data['username']
        password = data['password']
        
        # Verify credentials
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            token = generate_token(username)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred'
        }), 500
