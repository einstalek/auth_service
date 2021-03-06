from flask_auth import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return self.username

    @staticmethod
    def get(username: str):
        user = User.query.filter_by(username=username).first()
        return user
