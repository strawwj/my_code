from app import app
from flask import render_template
@app.route('/')
def index():
	return render_template('index.html',title='自我介绍',name='wj',other='大骗子')
@app.route('/student')
def student():
	s_list = ['张三','李斯','王无','赵刘']
	return render_template('student.html',slist=s_list)
@app.route('/teacher')
def teacher():
	s_dic = {'name':'zhangsan','age':18,'sex':1}
	return render_template('teacher.html',s=s_dic)
@app.route('/teachers')
def teachers():
	s1 = {'name':'zhangsan','age':18,'sex':1}
	s2 = {'name':'lisi','age':28,'sex':0}
	s3 = {'name':'wangwu','age':28,'sex':1}
	s4 = {'name':'zha0liu','age':38,'sex':0}
	s_list = [s1,s2,s3,s4]
	return render_template('teachers.html',slist=s_list)
