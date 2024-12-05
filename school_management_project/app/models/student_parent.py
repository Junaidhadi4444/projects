from app.db import db

student_parent = db.Table('student_parent',  # Name of the junction table
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('parent_id', db.Integer, db.ForeignKey('parents.id'), primary_key=True)
)
