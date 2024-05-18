import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-cant-guess-this-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Stop db tracking to improve performance

# Config for deployment db
class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Non-persistent db for automated testing
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True