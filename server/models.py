from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

# Association table HeroPower

class HeroPower(db.Model, SerializerMixin):

    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)

    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)
     
    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates="hero_powers")

    # Serialization rules to prevent recursion

    serialize_rules = (
        "-hero.hero_powers",
        "-power.hero_powers",
    )

    # Validations
    VALID_STRENGTHS = ('Strong', 'Weak', 'Average')

    @validates('strength')
    def validate_stregnth(self, key, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError(f"'strength' must be one of {self.VALID_STRENGTHS}")
        return value




class Hero(db.Model, SerializerMixin):

    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Relationships
    hero_powers = db.relationship ('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    #Access powers directly via Assosciation
    powers = db.relationship ('Power', secondary='hero_powers', back_populates='heroes', viewonly=True)

    #Serialization rules to avoid recursion
    serialize_rules = (
        "-hero_powers.hero",
        "-powers.hero_powers",
    )
    

class Power(db.Model, SerializerMixin):

    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers', viewonly=True)

    serialize_rules = (
        '-hero_powers.power',
        '-heroes.hero_powers',
    )

    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value
        
        






