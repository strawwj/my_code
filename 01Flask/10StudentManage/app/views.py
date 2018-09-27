from app import app
from flask import render_template,url_for,redirect,flash
from .forms import AddTeacherForm, AddStudentForm
from app import db
from app.models import Teacher,Student
from flask import abort, request

@app.route('/')
def index() :
	return render_template('index.html')

@app.route('/students')
def students() :
	ss = Student.query.all()
	return render_template('students.html', ss=ss)

@app.route('/teachers')
def teachers() :
	ts = Teacher.query.all()
	return render_template('teachers.html', ts=ts)

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher() :
	form=AddTeacherForm()
	if form.validate_on_submit() :
		teacher = Teacher()
		teacher.name = form.name.data
		teacher.age = form.age.data
		db.session.add(teacher)
		db.session.commit()
		return redirect(url_for('.teachers'))

	return render_template('add_teacher.html', form=form)

@app.route('/delete_teacher')
def delete_teacher() :
	#GET新技能:前端如何给后端传数据
	#这里希望前端在访问delete_teacher路由的时候传进来teacher的id
	#如何传： <a href="{{url_for('delete_teacher', id=t.id)}}">删除</a>
	#如何收：id = request.args.get('id')
	#传数据的本质：GET方式 127.0.0.1:5000/delete_teacher?id=1
	id = request.args.get('id')
	#如果用户访问的是127.0.0.1:5000/delete_teacher
	if id is None :
		abort(404)
	teacher = Teacher.query.filter_by(id=int(id)).first()
	if teacher is None :
		abort(404)
	
	db.session.delete(teacher)
	db.session.commit()

	return redirect(url_for('.teachers'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student() :
	form = AddStudentForm()
	if form.validate_on_submit() :
		teacher = Teacher.query.filter_by(name=form.teacher_name.data).first()
		if teacher is None :
			abort(404)
		student = Student()
		student.name = form.name.data
		student.teacher = teacher
		student.age = form.age.data
		student.sex = form.sex.data
		db.session.add(student)
		db.session.commit()
		return redirect(url_for('.students'))

	return render_template('add_student.html', form=form)

@app.route('/delete_student')
def delete_student() :
	id = request.args.get('id')
	#如果用户访问的是127.0.0.1:5000/delete_teacher
	if id is None :
		abort(404)
	student = Student.query.filter_by(id=int(id)).first()
	if student is None :
		abort(404)
	
	db.session.delete(student)
	db.session.commit()

	return redirect(url_for('.students'))

@app.route('/display_student')
def display_student():
	id = request.args.get('id')
	if id is None:
		abort(404)
	ss = Student.query.filter_by(teacher_id=id).all()
	if teachers is None:
		abort(404) 
	return render_template('display_student.html',ss=ss)

