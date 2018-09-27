from app import app
from flask import render_template
from .forms import RegisterForm
#重定向
from flask import redirect
from flask import url_for


#这个函数在两种情况下会被调用
#1.用户访问register路由(请求表单)
#2.提交表单
@app.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		#这段代码只有在提交表单的情况下才执行
		name = form.name.data
		password = form.password.data
		password_again = form.password_again.data
		email = form.email.data
		print(name,password,password_again,email)
		form.name.data=''
		form.email.data=''
		#return redirect('/login')
		return redirect(url_for('.login'))
	return render_template('register.html',form=form)
@app.route('/login')
def login():
	return render_template('login.html')
