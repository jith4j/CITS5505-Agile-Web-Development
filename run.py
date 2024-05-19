from app import db, create_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Question
from config import DeploymentConfig

flaskApp = create_app(DeploymentConfig)

@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Question': Question}