from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import humanize

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
app.jinja_env.globals['humanize'] = humanize

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)

    return app