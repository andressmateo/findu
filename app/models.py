from app import (db,app)
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user',
        'with_polymorphic': '*'
    }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'admin'}

class University(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    background = db.Column(db.Text)
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
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('places', lazy='dynamic'))
    background = db.Column(db.Text)

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


career_at_headquarter = db.Table('career_at_headquarter', db.metadata,
    db.Column('id_cat_university', db.Integer, db.ForeignKey('career_at_university.id')),
    db.Column('id_university_headquarter', db.Integer, db.ForeignKey('universityheadquarter.id'))
)


class CareerAtUniversity(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    description = db.Column(db.Text)
    graduates = db.Column(db.Integer)
    price = db.Column(db.Float)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    university = db.relationship('University', backref=db.backref('careers', lazy='dynamic'))
    #place_id = db.Column(db.Integer, db.ForeignKey('universityheadquarter.id'))
    #place = db.relationship('UniversityHeadquarter', backref=db.backref('careers', lazy='dynamic'))
    places = db.relationship("UniversityHeadquarter", secondary=career_at_headquarter, backref=db.backref('careers', lazy='dynamic'))
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    career = db.relationship('Career', backref=db.backref('places', lazy='dynamic'))

    def __init__(self, description, university, career, places=None, price=0, graduates=0):
        self.description = description
        self.graduates = graduates
        self.price = price
        self.university = university
        self.career = career
        self.places = places
        print "New CareerAtUniversity: "+self.__repr__()

    def __repr__(self):
        return "<CareerAtUniversity "+self.career.name+" >"


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