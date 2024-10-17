from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Blacklist(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    client_app_id = db.Column(db.String(200), nullable=False)
    blocked_reason = db.Column(db.String(255))
    origin_ip = db.Column(db.String(20), nullable=False)
    blacklist_timestamp = db.Column(db.DateTime, nullable=False)

