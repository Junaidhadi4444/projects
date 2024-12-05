from app.db import db

class Parent(db.Model):
    __tablename__='parents'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    husband_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    # Many-to-Many relationship with Student
    students = db.relationship('Student', secondary='student_parent', back_populates='parents')
    
    def __repr__(self):
        return f'<Parent {self.full_name}>'
