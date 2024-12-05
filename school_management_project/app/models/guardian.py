from app.db import db

class Guardian(db.Model):
    __tablename__='guardians'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(100), nullable=True)
    husband_name = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f'<Guardian {self.full_name}>'
