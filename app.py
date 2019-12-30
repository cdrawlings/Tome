from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_mail import Mail, Message
from threading import Thread
import os
import pymysql
from  flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'open sesame'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rawlings:1234@localhost:8889/tomeDB'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.fatcow.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dev@rawlings.site'
app.config['MAIL_PASSWORD'] = 'Test1Test'
app.config['MAIL_DEBUG'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['APP_MAIL_SUBJECT_PREFIX'] = '[Adventures Tome]'
app.config['APP_ADMIN'] = 'c.d.rawlings@gmail.com'
app.config['APP_MAIL_SENDER'] = 'Adventures Tome Admin <dev@rawlings.site>'
app.config['TESTING'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['APP_MAIL_SUBJECT_PREFIX'] +  subject,
                  sender=app.config['APP_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('Users', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Roles {}>'.format(self.name)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Users {}>'.format(self.username)


class LogIn(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', "POST"])
def login():
    form = LogIn()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.name.data).first()
        if user is None:
            user = Users(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['APP_ADMIN']:
                send_email(app.config['APP_ADMIN'], 'New User', 'mail/new_user',  user=user)
            else:
                session['known'] = True
                session['name'] = form.name.data
                form.name.data = ''
                return redirect(url_for('login'))
    return render_template('login.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
