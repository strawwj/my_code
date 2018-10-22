from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo,Length
from wtforms.validators import ValidationError
from app.models import User, Role


class EditUserForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Email(), Length(1, 128)])
    name = StringField(label='昵称', validators=[DataRequired(), Length(1, 128)])
    location = StringField(label='位置', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField(label='签名', validators=[DataRequired(), Length(1, 256)])
    # coerce=int 选择产生的是一个数字
    role_id = SelectField(label='角色', coerce=int)
    confirmed = BooleanField(label='邮箱激活')
    password = PasswordField(label='密码')
    password_again = PasswordField(label='确认密码', validators=[EqualTo('password', '两次密码不一致')])
    submit = SubmitField(label='确认编辑')

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]


class AddUserFrom(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Email(), Length(1, 128)])
    name = StringField(label='昵称', validators=[DataRequired(), Length(1, 128)])
    location = StringField(label='位置', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField(label='签名', validators=[DataRequired(), Length(1, 256)])
    # coerce=int 选择产生的是一个数字
    role_id = SelectField(label='角色', coerce=int)
    confirmed = BooleanField(label='邮箱激活')
    password = PasswordField(label='密码')
    submit = SubmitField(label='确认编辑')

    def __init__(self, *args, **kwargs):
        super(AddUserFrom, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]


class SearchForm(FlaskForm):
    email = StringField(label='邮箱', validators=[Email(), Length(1, 128)])
    submit = SubmitField(label='搜素')