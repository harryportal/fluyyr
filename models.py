import datetime
import enum
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce_for_enum(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

class Genre(enum.Enum):
    Alternative = 'Alternative'
    Blue = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RandB = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'


class State(enum.Enum):
    AR = 'AR'
    AZ = 'AZ'
    AK = 'AK'
    AL = 'AL'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(State), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(MutableList.as_mutable(ARRAY(db.Enum(Genre))), nullable=False)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120), default=None)
    facebook_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(200), default=None)
    date_created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.Enum(State), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(MutableList.as_mutable(ARRAY(db.Enum(Genre))), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    show_time = db.Column(db.DateTime(), nullable=False)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
