from app import app
from flask import render_template
@app.route('/')
def macro():
	t1={"name":"zhangsan","age":28,"sex":1}
	t2={"name":"lisi","age":28,"sex":1}
	t3={"name":"wangwu","age":18,"sex":0}
	t4={"name":"zhaoliu","age":28,"sex":0}
	t_list=[t1,t2,t3,t4]
	return render_template('index.html',tlist=t_list)
