from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/breakfasts_development'
    app.config['SQLALCHEMY_ECHO'] = True
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.breakfast import Breakfast

    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app