from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type = db.Column(db.String(100))
    potholes = relationship('pothole')
    
class Pothole(db.Model):
    __tablename__ = 'pothole'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    streetNumber = db.Column(db.Integer)
    streetName = db.Column(db.Text)
    state = db.Column(db.String(2))
    city = db.Column(db.String(10))
    zip = db.Column(db.Integer)
    size = db.Column(db.Integer)
    location = db.Column(db.String(100))
    district = db.Column(db.String(100))
    priority = db.Column(db.String(100))
    workorder = relationship("WorkOrder", uselist=False, back_populates="pothole")
    
class RepairCrew(db.Model):
    __tablename__ = 'repair_crew'
    id = db.Column(db.Integer, primary_key=True)
    people = db.Column(db.Integer)
    workorder = relationship("WorkOrder", uselist=False, back_populates="repair_crew")
    
class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    equipment = db.Column(db.String(100))
    
class WorkOrder(db.Model):
    __tablename__ = 'work_order'
    id = db.Column(db.Integer, primary_key=True)
    pothole_id = db.Column(db.Integer, ForeignKey('pothole.id'))
    pothole = relationship("Pothole", back_populates="work_order")
    repair_crew_id = db.Column(db.Integer, ForeignKey('repair_crew.id'))
    repair_crew = relationship("RepairCrew", back_populates="work_order")
    equipment_id = db.Column(db.Integer, ForeignKey('equipment.id'))
    equipment = relationship("Equipment", back_populates="work_order")
    hours = db.Column(db.Integer)
    status = db.Column(db.String(100))
    fillerAmount = db.Column(db.Integer)
    cost=db.Column(db.Float)
    
    
