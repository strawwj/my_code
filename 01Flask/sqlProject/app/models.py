from app import db
class Student(db.Model):
	__tablename__='students'
	id = db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(32))
	teacher_id=db.Column(db.Integer,db.ForeignKey('teachers.id'))
	def __str__(self):
		return self.name+':'+str(self.id)
class Teacher(db.Model):
	__tablename__='teachers'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(32))
	#反向关系：在一对多中，假设一个老师对应多个学生
	#关联学生表，向Student模型中添加一个teacher属性（但这个属性并不会出现在表中，students属性也不会出现在表teachers中）
	#定义反向关系，students属性将返回相关联的Student组成的列表
	students=db.relationship('Student',backref='teacher',lazy='dynamic')
	def __str__(self):
		return self.name+':'+str(self.id)
