from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, Blacklist

class AddToBlacklist(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json

        mail = Blacklist(
            email = data.get("email"),
            client_app_id = data.get("app_uuid"),
            blocked_reason = data.get("blocked_reason"),
            origin_ip = "127.0.0.1",
            blacklist_timestamp = datetime.now()
        )
        db.session.add(mail)
        db.session.commit()

        return {
            "message": "Account created"
        }, 201
