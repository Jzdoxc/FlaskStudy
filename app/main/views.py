from datetime import datetime
from flask import session, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.decorators import admin_required, permission_required
from . import main
from ..models import User, Permission
from .forms import EditProfileForm, EditProfileAdminForm


@main.route('/', methods=['GET', 'POST'])
def index():
    # form=NameForm()
    # if form.validate_on_submit():
    #     user=User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user=User(username=form.name.data)
    #         db.session.add(user)
    #         session['known']=False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_mail(main.config['FLASKY_ADMIN'],'新的用户','mail/new_user',user=user)
    #     else:
    #         session['known']=True
    #     session['name']=form.name.data
    #     form.name.data=''
    #     return redirect(url_for('.index'))
    return render_template('index.html', name=session.get('name'), current_time=datetime.utcnow())


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For administrators"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators"


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("你的帐户资料已更新")
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("用户的资料已经被更新")
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
