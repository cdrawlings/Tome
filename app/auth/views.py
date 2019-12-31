from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import Users
from .forms import LogIn

@auth.route('/login', methods=['GET', "POST"])
def login():
    form = LogIn()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
           login_user(user, form.remember_me.data)
           next = request.args.get('next')
           if next is None or not next.startswith('?'):
               next = url_for('main.index')
           return redirect(next)
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out')
    return redirect(url_for('main.index'))