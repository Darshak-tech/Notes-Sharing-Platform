from flask import Flask
from config import Config
from models import db, login_manager
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.api import api_bp
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
