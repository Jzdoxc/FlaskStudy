from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from ..models import User, db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        # 注册后自动登陆
        db.session.commit()
        # login_user(user)
        flash("你已经可以登陆了")
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'mail/new_user', user=user, token=token)
        flash('注册邮箱确认邮件已发送至你的邮箱，请确认邮件.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认了你的邮箱，谢谢！')
    else:
        flash('确认链接无效！.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'mail/new_user', user=current_user, token=token)
    flash('一封新的邮件已发送至您的邮箱')
    return redirect(url_for('main.index'))


@auth.route('/secret')
@login_required
def secret():
    return '登陆后才可以查看'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经注销了')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash("你的密码已经更新")
            return redirect(url_for('main.index'))
        else:
            flash("你的旧密码不正确")
    return render_template("auth/change-password.html", form=form)
