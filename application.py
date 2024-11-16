from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models.models import db
from views.health_check import HealthCheck
from views.add_to_blacklist import AddToBlacklist
from views.check_blacklist import CheckBlacklist

import os

def create_app():
    application = Flask(__name__)

    host = os.environ.get('RDS_HOSTNAME', 'awseb-e-2czu7iuywm-stack-awsebrdsdatabase-yeqkvxnsagvf.crms4uw0o5aq.us-east-2.rds.amazonaws.com')
    port = os.environ.get('RDS_PORT', '5432')
    dbName = os.environ.get('RDS_DB_NAME', 'ebdb')
    username = os.environ.get('RDS_USERNAME', 'postgres')
    password = os.environ.get('RDS_PASSWORD', 'Password123!')

    application.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{username}:{password}@{host}:{port}/{dbName}'
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.config["JWT_SECRET_KEY"] = "frase-secreta"
    application.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    if not os.environ.get('TESTING'):
        init_db(application)

    add_routes(application)

    jwt = JWTManager(application)
    return application


def add_routes(application):
    api = Api(application)
    api.add_resource(HealthCheck, "/ping")
    api.add_resource(AddToBlacklist, "/blacklists")
    api.add_resource(CheckBlacklist, "/blacklists/<string:email>")

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0', port='5000')
