from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions with app
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
    # Import and register blueprints
    from .routes import auth, accounts, transactions, admin
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(accounts.bp, url_prefix='/api/accounts')
    app.register_blueprint(transactions.bp, url_prefix='/api/transactions')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
