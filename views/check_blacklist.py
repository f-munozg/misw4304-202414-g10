
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.models import Blacklist


class CheckBlacklist(Resource):
    @jwt_required()
    def get(self, email):
        current_user = get_jwt_identity()
        mail = Blacklist.query.filter(
            Blacklist.email == email
        ).first()

        if mail is None:
            return {"mail_blacklisted": False}, 401
        
        return {
            "mail_blacklisted": True,
            "blacklist_reason": mail.blocked_reason
        }, 200