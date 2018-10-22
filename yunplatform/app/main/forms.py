from wtforms import StringField, TextAreaField, SubmitField, IntegerField,SelectField, BooleanField, FileField
from wtforms import PasswordField, FloatField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo
from app.models import Sensor
from flask_wtf.file import FileAllowed, FileRequired
# from app import uploadset

# 编辑用户表单
class EditUserForm(FlaskForm):
    name = StringField(label='昵称', validators=[DataRequired(), Length(1, 128)])
    password = PasswordField(label='密码')
    password_again = PasswordField(label='确认密码', validators=[EqualTo('password', '两次密码不一致')])
    about_me = TextAreaField(label='关于我', validators=[DataRequired(), Length(1, 256)])
    location = StringField(label='位置', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField(label='确认编辑')


# 新闻表单
class PostNewsForm(FlaskForm):
    title = StringField(label='标题', validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField(label='正文', validators=[DataRequired(),Length(1, 256)])
    private = BooleanField(label='私有', default=False)
    submit = SubmitField(label='发表')


# 设备表单, 编辑设备
class DeviceForm(FlaskForm):
    name = StringField(label='设备名称', validators=[DataRequired(), Length(1, 128)])
    describe = TextAreaField(label='设备描述', validators=[DataRequired()])
    location = StringField(label='设备位置', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField(label='添加设备')


# 传感器表单
class SensorForm(FlaskForm):
    name = StringField(label='传感器名称', validators=[DataRequired(), Length(1, 128)])
    unit = StringField(label='测量单位', validators=[DataRequired()])
    describe = TextAreaField(label='传感器描述', validators=[DataRequired()])
    submit = SubmitField(label='添加传感器')


# 编辑传感器表单
class EditSensorForm(FlaskForm):
    name = StringField(label='传感器名称', validators=[DataRequired(), Length(1, 128)])
    unit = StringField(label='测量单位', validators=[DataRequired(), Length(1, 128)])
    describe = TextAreaField(label='传感器描述', validators=[DataRequired()])
    max = FloatField(label='最大值', validators=[DataRequired()])
    min = FloatField(label='最小值', validators=[DataRequired()])
    submit = SubmitField(label='编辑传感器')


class SearchForm(FlaskForm):
    data = StringField(label='传感器', validators=[Length(1, 128)])
    submit = SubmitField(label='搜素')


class HeadImageForm(FlaskForm):
 pic_name = StringField('fileName', validators=[DataRequired()])
 #上传文件控件
 file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png']), FileRequired()])
 submit = SubmitField('submit')
# class HeadImageForm(FlaskForm) :
#  fileName = StringField('fileName', validators=[DataRequired()])
#  file = FileField('file', validators=[FileAllowed(uploadset, '文件类型有误'),
# FileRequired()])
#  submit = SubmitField('submit')