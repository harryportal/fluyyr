from datetime import datetime
from flask_wtf import Form
from models import Genre, State
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, Regexp

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(v, v.value) for v in State]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[(v, v.value) for v in Genre]
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    website_link = StringField(
        'website_link',  validators=[Optional(), URL()]
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(v, v.value) for v in State]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[(v, v.value) for v in Genre]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link'
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
            'seeking_description'
     )