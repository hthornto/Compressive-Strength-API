from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create your models here.


class Sets(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slump = db.Column(db.Float, nullable=True)
    air_content = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Integer, nullable=True)
    ticket_number = db.Column(db.Integer, nullable=True)
    mix_id = db.Column(db.Integer, db.ForeignKey(
        'mix_design.id'), nullable=False)
    total_cy = db.Column(db.Integer, nullable=True)
    project_id = db.Column(db.String, nullable=True)
    field_tech_id = db.Column(db.Integer, nullable=True)
    mix_used_id = db.Column(
        db.Integer, db.ForeignKey("mix_used.id"), nullable=True)
    cylinders = db.relationship(
        "Cylinders", backref="sets", cascade='all,delete')

    # mix_design = db.relationship(
    #    "Mix_design", backref="sets", cascade='all,delete')

    """def __init__(self, mix_id, slump=None, air_content=None, temperature=None, ticket_number=None, total_cy=None, project_id=None, field_tech=None, mix_used_id=None):
        self.mix_id = mix_id
        self.slump = slump
        self.air_content = air_content
        self.temperature = temperature
        self.ticket_number = ticket_number
        self.total_cy = total_cy
        self.project_id = project_id
        self.field_tech_id = field_tech
        self.mix_used_id = mix_used_id
"""

    def serialize(self):
        return {
            'id': self.id,
            'slump': self.slump,
            'air_content': self.air_content,
            'temperature': self.temperature,
            'ticket_number': self.ticket_number,
            'mix_id': self.mix_id,
            'total_cy': self.total_cy,
            'project_id': self.project_id,
            'field_tech_id': self.field_tech_id,
            'mix_used_id': self.mix_used_id,
            "cylinders": self.air_content
            # "isMRWH": self.isMRWH,
            # "isHRWH": self.isHRWH
        }


class Cylinders(db.Model):
    __tablename__ = 'cylinders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), nullable=False)
    max_load = db.Column(db.Integer, nullable=True)
    dia1 = db.Column(db.Float, nullable=True)
    dia2 = db.Column(db.Float, nullable=True)
    break_strength = db.Column(db.Integer, nullable=True)
    # Move cylinder type to sets
    cylinder_type_id = db.Column(
        db.Integer, db.ForeignKey('specimen_type.id'), nullable=False)
    break_type = db.Column(db.String, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    lab_tech_id = db.Column(db.Integer, nullable=True)
    recieved = db.Column(db.Date, nullable=True)
    break_age = db.Column(db.Integer, nullable=False)
    on_hold = db.Column(db.Boolean, nullable=False)

    def __init__(self, set_id, break_age, on_hold, max_load=None, dia1=None, dia2=None, break_strength=None, cylinder_type_id=None, break_type=None, weight=None, lab_tech_id=None, recieved=None):

        self.set_id = set_id
        self.max_load = max_load
        self.dia1 = dia1
        self.dia2 = dia2
        self.break_strength = break_strength
        self.cylinder_type_id = cylinder_type_id
        self.break_type = break_type
        self.weight = weight
        self.lab_tech_id = lab_tech_id
        self.recieved = recieved
        self.break_age = break_age,
        self.on_hold = on_hold

    def serialize(self):
        return {
            "id": self.id,
            "set_id": self.set_id,
            "max_load": self.max_load,
            "dia1": self.dia1,
            "dia2": self.dia2,
            "break_strength": self.break_strength,
            "cylinder_type_id": self.cylinder_type_id,
            "break_type": self.break_type,
            "weight": self.weight,
            "lab_tech_id": self.lab_tech_id,
            "recieved": self.recieved,
            "age": self.break_age,
            "hold": self.on_hold,
        }


class Specimen_Type(db.Model):
    __tablename__ = "specimen_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    speciman_type = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=False)
    cylinders = db.relationship(
        "Cylinders", backref="specimen_type", cascade='all,delete')

    def __init__(self, speciman_type, size):
        self.speciman_type = speciman_type
        self.shape = size

    def serialize(self):
        return {
            "id": self.id,
            "type": self.speciman_type,
            'size': self.shape,
        }


class MixDesign(db.Model):
    __tablename__ = "mix_design"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # mix_description = db.Column(db.String, nullable=True)
    # mix_code = db.Column(db.String, nullable=True)
    producer = db.Column(db.String, nullable=False)
    max_slump = db.Column(db.Float, nullable=True)
    min_slump = db.Column(db.Float, nullable=True)
    min_air_content = db.Column(db.Float, nullable=True)
    max_air_content = db.Column(db.Float, nullable=True)
    mid_range_max_slump = db.Column(db.Float, nullable=True)
    mid_range_min_slump = db.Column(db.Float, nullable=True)
    high_range_max_slump = db.Column(db.Float, nullable=True)
    high_range_min_slump = db.Column(db.Float, nullable=True)
    project_id = db.Column(db.String, nullable=False)
    sets = db.relationship("Sets", backref='mix_design', cascade="all,delete")
    design_strength = db.Column(db.Integer, nullable=False)
    break_schedule = db.Column(db.JSON, nullable=False)
    """
    method to use for break schedule
    age = [
        {'age':7, 'hold': False},
        {'age':28, 'hold': False},
        {'age':28, 'hold': False},
        {'age':28, 'hold': False},
        {'age':28, 'hold': True},
    ]
    """

    # set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=True)

    """def __init__(self, project_id, design_strength, producer=None, max_slump=None):
        self.project_id = project_id
        self.design_strength = design_strength
        self.producer = producer
        self.max_slump = max_slump
"""

    def serialize(self):
        return {
            "id": self.id,
            # 'mix description': self.mix_description,
            "producer":  self.producer,
            # "mix code": self.mix_code,
            "max slump": self.max_slump,
            "min slump": self.min_slump,
            "max air content": self.max_air_content,
            "min air content": self.min_air_content,
            "MRWH max slump": self.mid_range_max_slump,
            "MRWH min slump": self.mid_range_min_slump,
            "HRWH max slump": self.high_range_max_slump,
            "HRWH min slump": self.high_range_min_slump,
            "design_strength": self.design_strength,
            "project_id": self.project_id,
            "break_schedule": self.break_schedule
            # "set_id": self.set_id,
            # "sets": self.sets

        }


class MixUsed(db.Model):
    __tablename__ = "mix_used"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mix_description = db.Column(db.String, nullable=True)
    mix_code = db.Column(db.String, nullable=True)
    producer = db.Column(db.String, nullable=False)
    strength = db.Column(db.Integer, nullable=True)
    isMRWH = db.Column(db.Boolean, nullable=False)
    isHRWH = db.Column(db.Boolean, nullable=False)
    sets = db.relationship("Sets", backref='mix_used', cascade="all,delete")

    def __init__(self, producer, mix_description=None, mix_code=None, strength=None, isMRWH=False, isHRWH=False):
        self.producer = producer
        self.mix_description = mix_description
        self.mix_code = mix_code
        self.strength = strength
        self.isMRWH = isMRWH
        self.isHRWH = isHRWH

    def serialize(self):
        return {
            "id": self.id,
            "producer": self.producer,
            "mix_description": self.mix_description,
            "mix_code": self.mix_code,
            "strength": self.strength,
            "isMRWH": self.isMRWH,
            "isHRWH": self.isHRWH,
            # "sets": self.sets,
        }


class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(2), nullable=True)
    postalcode = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    projects = db.relationship(
        "Projects", backref='clients', cascade="all,delete")

    """def __init__(self, name: str, address: str, country: str, postalcode: str, city: str):
        self.name = name
        self.address = address
        self.country = country
        self.postalcode = postalcode
        self.city = city
"""

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "postalcode": self.postalcode,
            "country": self.country
        }


class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'clients.id'), nullable=False)
    # project_type = db.Column(db.Integer,  nullable=False)

    def __init__(self, name: str, client_id: int):
        self.name = name
        self.client_id = client_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "client_id": self.client_id
        }
