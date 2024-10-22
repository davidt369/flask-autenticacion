import os
from flask import Flask, jsonify
from models import db
from flask_jwt_extended import JWTManager
from views import auth_bp
from config import Config
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'El token ha expirado'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido'}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Se requiere un token de acceso'}), 401

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))


