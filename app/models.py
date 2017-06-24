from app import db


class User(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    nickname= db.Column(db.String(64), index = True)
