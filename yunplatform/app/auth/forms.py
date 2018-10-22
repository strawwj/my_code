from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo,Length
from wtforms.validators import ValidationError
from app.models import User


class LoginFrom(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(6, 128), Email()])
    password = PasswordField(label='密码', validators=[DataRequired(), Length(1, 128)])
    remember_me = BooleanField(label='记住我')
    submit = SubmitField(label='登陆')


class RegisterForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(6, 128), Email()])
    name = StringField(label='昵称', validators=[DataRequired(),Length(2, 128)])
    password = PasswordField(label='密码', validators=[DataRequired(), Length(1,128)])
    password_again = PasswordField(label='确认密码', validators=[EqualTo('password', '两次密码不统一请重新输入')])
    submit = SubmitField(label='注册')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('这个邮箱已经被注册')