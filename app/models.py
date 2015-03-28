from app import db
from app import app

class University(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    background = db.Column(db.Text)
    #News
    motto = db.Column(db.Text)
    established = db.Column(db.Integer)
    type = db.Column(db.String(100))  # privada - publica.
    principal = db.Column(db.String(200))
    students = db.Column(db.Integer)
    web_site = db.Column(db.Text)
    address = db.Column(db.String(100))
    accredited = db.Column(db.Boolean)
    facebook = db.Column(db.Text)
    twitter = db.Column(db.Text)
    #places object, places.all()
    #names object, names.all()

    def __init__(self, name, description, logo, background="", motto="", established=0, type="", principal ="",
                 students=0, web_site="", address="", accredited=False, facebook="", twitter=""):
        self.name = name
        self.description = description
        self.logo = logo
        self.background = background
        self.motto = motto
        self.established = established
        self.type = type
        self.principal = principal
        self.students = students
        self.web_site = web_site
        self.address = address
        self.accredited = accredited
        self.facebook = facebook
        self.twitter = twitter
        print "New University: "+self.__repr__()

    def __repr__(self):
        return "<University "+self.name+" >"


class KnowledgeArea(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    definition = db.Column(db.Text)

    def __init__(self, name, definition):
        self.name = name
        self.definition = definition
        print "New KnowledgeArea: "+self.__repr__()

    def __repr__(self):
        return "<KnowledgeArea "+self.name+" >"


related = db.Table('related', db.metadata,
    db.Column('id_career', db.Integer, db.ForeignKey('career.id')),
    db.Column('id_knowledge_area', db.Integer, db.ForeignKey('knowledge_area.id'))
)


class Career(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    type = db.Column(db.String(40))
    description = db.Column(db.Text)
    knowledge_areas = db.relationship("KnowledgeArea", secondary=related, backref=db.backref('careers', lazy='dynamic'))
    icon = db.Column(db.Text)
    background = db.Column(db.Text)
    #places object, places.all()

    def __init__(self, name, type, description, knowledge_areas=None, icon="", background=""):
        self.name = name
        self.description = description
        self.type = type  # PREGRADO-POSGRADO-ETC
        self.knowledge_areas = knowledge_areas
        self.icon = icon
        self.background = background
        print "New Career: "+self.__repr__()

    def __repr__(self):
        return "<Career "+self.name+" >"


class UniversityHeadquarter(db.Model):
    __tablename__ = "universityheadquarter"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    campus_name = db.Column(db.String(200))
    lat = db.Column(db.Float)  # Latitude
    long = db.Column(db.Float)  # Longitude
    #careers object, careers.all()
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('places', lazy='dynamic'))
    background = db.Column(db.Text)
    #images object, images.all()

    def __init__(self, campus_name, lat, long, university, background=""):
        self.lat = lat
        self.long = long
        self.university = university
        self.campus_name = campus_name
        self.background = background
        print "New Headquarter: "+self.__repr__()

    def __repr__(self):
        return "<Headquarter "+self.campus_name+" >"


class OtherName(db.Model):
    name = db.Column(db.String(200), unique=True, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('names', lazy='dynamic'))

    def __init__(self, name, university):
        self.name = name
        self.university = university
        print "New Name: "+self.__repr__()

    def __repr__(self):
        return "<Name "+self.name+" >"


class CareerAtUniversity(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    description = db.Column(db.Text)
    graduates = db.Column(db.Integer)
    price = db.Column(db.Float)
    place_id = db.Column(db.Integer, db.ForeignKey('universityheadquarter.id'))
    place = db.relationship('UniversityHeadquarter', backref=db.backref('careers', lazy='dynamic'))
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    career = db.relationship('Career', backref=db.backref('places', lazy='dynamic'))

    def __init__(self, description, place, career, price=0, graduates=0):
        self.description = description
        self.graduates = graduates
        self.price = price
        self.place = place
        self.career = career
        print "New CareerAtUniversity: "+self.__repr__()

    def __repr__(self):
        return "<CareerAtUniversity "+self.career.name+"@"+self.place.university.name+" >"


class ImageCampus(db.Model):
    src = db.Column(db.Text, unique=True, primary_key=True)
    title = db.Column(db.Text)
    alt = db.Column(db.Text)
    description = db.Column(db.Text)
    source = db.Column(db.Text)
    campus_id = db.Column(db.Integer, db.ForeignKey('universityheadquarter.id'))
    campus = db.relationship('UniversityHeadquarter', backref=db.backref('images', lazy='dynamic'))

    def __init__(self, campus, src, title="", alt="Image", description="", source=""):
        self.campus = campus
        self.src = src
        self.title = title
        self.alt = alt
        self.description = description
        self.source = source
        print "Image Added: "+self.__repr__()

    def __repr__(self):
        return "<Image of "+self.campus.campus_name+" @"+self.src+" >"