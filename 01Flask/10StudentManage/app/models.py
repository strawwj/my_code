from app import db
class Student(db.Model):
	__tablename__='students'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	age = db.Column(db.Integer)
	teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'))
	sex = db.Column(db.Integer,default=1)
class Teacher(db.Model):
	__tablename__ = 'teachers'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	age = db.Column(db.Integer)
	students = db.relationship('Student',backref='teacher',lazy='dynamic')
