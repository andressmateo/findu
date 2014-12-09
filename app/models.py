from app import db
from app import app

class Team(db.Model):
    username = db.Column(db.String(140),unique=True,primary_key=True)
    age = db.Column(db.Integer)
    level = db.Column(db.Integer)
    def __init__(self,user,age,level=0):
        self.username = user
        self.age = age
        self.level = level
        print "New User: "+self.__repr__()
    def __repr__(self):
        return '<Team %r>'%(self.username)

class University(db.Model):
    id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    #places object, places.all()
    #names object, names.all()
    def __init__(self,name,description,logo):
        self.name = name
        self.description = description
        self.logo = logo
        print "New University: "+self.__repr__()
    def __repr__(self):
        return "<University "+self.name+" >"

class Career(db.Model):
    id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    type = db.Column(db.String(40))
    description = db.Column(db.Text)
    #places object, places.all()
    def __init__(self,name,type,description):
        self.name = name
        self.description = description
        self.type = type #PREGRADO-POSGRADO-ETC
        print "New Career: "+self.__repr__()
    def __repr__(self):
        return "<Career "+self.name+" >"

class UniversityHeadquarter(db.Model):
    __tablename__ = "universityheadquarter"
    id = db.Column(db.Integer,unique=True,primary_key=True)
    lat = db.Column(db.Float) #Latitude
    long = db.Column(db.Float) #Longitude
    #careers object, careers.all()
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('places', lazy='dynamic'))
    def __init__(self,lat,long,university):
        self.lat = lat
        self.long = long
        self.university = university
        print "New Headquarter: "+self.__repr__()
    def __repr__(self):
        return "<Headquarter>"

class OtherName(db.Model):
    name = db.Column(db.String(200),unique=True,primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('names', lazy='dynamic'))
    def __init__(self,name,university):
        self.name = name
        self.university = university
        print "New Name: "+self.__repr__()
    def __repr__(self):
        return "<Name "+self.name+" >"

class CareerAtUniversity(db.Model):
    id = db.Column(db.Integer,unique=True,primary_key=True)
    description = db.Column(db.Text)
    graduates = db.Column(db.Integer)
    price = db.Column(db.Float)
    place_id = db.Column(db.Integer, db.ForeignKey('universityheadquarter.id'))
    place = db.relationship('UniversityHeadquarter', backref=db.backref('careers', lazy='dynamic'))
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    career = db.relationship('Career', backref=db.backref('places', lazy='dynamic'))

    def __init__(self,description,place,career,price = 0,graduates=0):
        self.description = description
        self.graduates = graduates
        self.price = price
        self.place = place
        self.career = career
        print "New CareerAtUniversity: "+self.__repr__()
    def __repr__(self):
        return "<CareerAtUniversity>"