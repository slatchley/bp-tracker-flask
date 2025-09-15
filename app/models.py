from app import db
from datetime import datetime

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    pulse = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Reading {self.id} {self.systolic}/{self.diastolic} {self.pulse}>"