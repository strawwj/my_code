#1.导入flask
from flask import Flask
#2.构建flask对象
#flask对象中socket，能有与浏览器建立连接
#能够接收浏览器的数据，并且能够发送数据给浏览器
#浏览器和web服务器之间的数据符合http协议
#flask对象能够解决http协议
app = Flask(__name__)
#3.定义视图函数并且添加路由
@app.route('/abc')
def index():
	return 'hello flask'
@app.route('/')
def root():
	return '''
		<h1>这是一个标题</h1>
		<p>这是一个段落</p>
'''
#如何渲染前端工程师写好的页面
#a在test.py同级目录下创建templates和static文件夹
#b把*.html文件放到templates文件夹中
#c把其他文件夹放到static文件夹
#d构建一个视图函数并且添加一个路由
#e.替换css js imgages的路径
#:把css/替换成/static/css/
#:%s/css\//\/static\/css\//g

from flask import render_template
@app.route('/bp')
def bp():
	#把index.html的内容读出来做成字符串，然后返回 发送给浏览器
	#注意：render_template默认去template找文件
	return render_template('index.html')
#127.0.0.1:5000/add/4/5
#动态路由的变量有三种类型：int float path
@app.route('/add/<int:a>/<int:b>')
def add(a,b):
	return str(a+b)
#4.运行
app.run(debug=True)
#app.run(host='172.25.4.216',port= 5000,debug=True)

