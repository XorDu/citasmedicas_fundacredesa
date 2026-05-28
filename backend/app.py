import os
from flask import Flask
from backend.config import config
from backend.database import db, login_manager
from backend.models import User

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
    
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes
    from backend.routes.auth import auth_bp
    from backend.routes.admin import admin_bp
    from backend.routes.appointments import appointments_bp
    from backend.routes.calendar import calendar_bp
    from backend.routes.patients import patients_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.historias import historias_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(historias_bp)

    return app
