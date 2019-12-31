from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager, db


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('Users', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Roles {}>'.format(self.name)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))