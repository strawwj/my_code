from flask import render_template
from flask import url_for,redirect
from app import app
@app.route('/')
def index():
	return 'ok'
