from flask import session, redirect, url_for, render_template, current_app
from app.decorators import admin_required, permission_required
from flask_login import login_required

from ..models import User, Permission
from .. import db
from . import main
from datetime import datetime
from .forms import NameForm
from ..email import send_email


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
