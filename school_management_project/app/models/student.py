from app.db import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    guardian_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False)

    class_id=db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    # Many-to-Many relationship with Parent
    parents = db.relationship('Parent', secondary='student_parent', back_populates='students')
    
    def __repr__(self):
        return f'<Student {self.full_name}>'
