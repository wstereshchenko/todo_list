from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(50))
    body = db.Column(db.String(500))
    now = datetime.now()
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def store_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_post(self):

        db.session.delete(self)
        db.session.commit()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))