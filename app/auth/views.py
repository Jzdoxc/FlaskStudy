from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from . import auth
from ..models import User, db
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        flash("你已经可以登陆了")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经注销了')
    return redirect(url_for('main.index'))
