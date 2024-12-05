from app.db import db

class Class(db.Model):
    __tablename__='classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(50), nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    students=db.relationship('Student', backref='class_', lazy=True)
    
    def __repr__(self):
        return f'<Class {self.class_name} - {self.section}>'
