from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Earthquake model
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = 'earthquakes'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Earthquake {self.id} - {self.location} - {self.magnitude}>'
