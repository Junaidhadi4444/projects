from app.db import db

class FeeStructure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fee = db.Column(db.Float, nullable=False)
    dues = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<FeeStructure for Class {self.fee}>'
