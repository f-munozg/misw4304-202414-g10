from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models.models import db, Blacklist

class AddToBlacklist(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        origin_ip = request.remote_addr
        print('request.remote_addr:', origin_ip)
        print(request.environ.get('HTTP_X_FORWARDED_FOR', "x_forwarded_not_Found"))
        print(request.headers.get('X-Forwarded-For', "x-forwarded-not-found"))
        data = request.json

        mail = Blacklist(
            email = data.get("email"),
            client_app_id = data.get("app_uuid"),
            blocked_reason = data.get("blocked_reason"),
            origin_ip = origin_ip,
            blacklist_timestamp = datetime.now()
        )
        try:
            db.session.add(mail)
            db.session.commit()
        except IntegrityError:
            return {
                "message": "Email is already blacklisted"
            }, 409

        return {
            "message": "Account created successfully"
        }, 201
