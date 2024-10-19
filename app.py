from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models.models import db
from views.add_to_blacklist import AddToBlacklist
from views.check_blacklist import CheckBlacklist

import os

def create_app():
    app = Flask(__name__)

    host = os.environ.get('RDS_HOSTNAME', 'awseb-e-d2cppafjze-stack-awsebrdsdatabase-rvisptomh3oc.crms4uw0o5aq.us-east-2.rds.amazonaws.com')
    port = os.environ.get('RDS_PORT', '5432')
    dbName = os.environ.get('RDS_DB_NAME', 'ebdb')
    username = os.environ.get('RDS_USERNAME', 'postgres')
    password = os.environ.get('RDS_PASSWORD', 'Password123!')

    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{username}:{password}@{host}:{port}/{dbName}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "frase-secreta"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app_context = app.app_context()
    app_context.push()
    add_routes(app)

    jwt = JWTManager(app)
    return app


def add_routes(app):
    api = Api(app)
    api.add_resource(AddToBlacklist, "/blacklists")
    api.add_resource(CheckBlacklist, "/blacklists/<string:email>")

app = create_app()
db.init_app(app)
db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
