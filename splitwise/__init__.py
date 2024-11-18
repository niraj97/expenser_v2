from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize core application components
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///splitwise.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes.auth import auth as auth_blueprint
    from .routes.expenses import expenses as expenses_blueprint
    from .routes.groups import groups as groups_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(expenses_blueprint, url_prefix='/expenses')
    app.register_blueprint(groups_blueprint, url_prefix='/groups')

    return app
