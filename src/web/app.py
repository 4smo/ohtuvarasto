"""Flask web application for warehouse management."""
import os
from flask import Flask
from web.models import db
from web.routes import register_routes


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    configure_app(app, config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    register_routes(app)
    return app


def configure_app(app, config):
    """Configure the Flask application."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'warehouse.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if config:
        app.config.update(config)


if __name__ == '__main__':
    application = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    application.run(debug=debug_mode)
