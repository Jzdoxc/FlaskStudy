from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError

from app.models import Role, User


class NameForm(Form):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Realname', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须包含数字，字母，或下划线')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Realname', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')
