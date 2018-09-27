from app import app #前app包 后对象

@app.route('/')
def index():
	return '这是主页'
