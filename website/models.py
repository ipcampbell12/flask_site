from . import db
from datetime import datetime

#define Animal model 
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    def __repr__(self):
        return '<Animal %r' % self.id