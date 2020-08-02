from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from handcam.config import Config

from handcam.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
    mail,
)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)    
    register_extensions(app)
    from handcam.users.routes import users
    from handcam.main.routes import main
    from handcam.annotator.routes import annotator
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(annotator)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db,compare_type=True)
    return None