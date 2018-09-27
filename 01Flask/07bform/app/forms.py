from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email
#继承FlaskFrom
class RegisterForm(FlaskForm):
	name = StringField(label='名字',validators=[DataRequired(),Length(1,64)])
	password = PasswordField(label='密码',validators=[DataRequired(),Length(6,128)])
	password_again=PasswordField(label='密码',validators=[EqualTo('password','两次密码不统一，请重新输入')])
	email = StringField(label='邮箱',validators=[DataRequired(),Length(1,128),Email('邮箱输入不正确')])
	submit = SubmitField(label='提交')
