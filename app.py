# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from datetime import datetime
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import Show, Artist, Area, Venue
from models import db

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
db.init_app(app)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(str(value))
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    # Shows Recent Listed Artists and Recently Listed Venues on the homepage, returning results
    # for Artists and Venues sorting by newly created. Limit to the 10 most recently
    # listed items.
    recent_artists = Artist.query.order_by(Artist.date_created).limit(10).all()
    recent_venues = Venue.query.order_by(Venue.date_created).limit(10).all()
    return render_template('pages/home.html', recent_artists=recent_artists, recent_venues=recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = Area.query.all()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    searched_term = request.form.get('search_term')
    response = (Venue.query.filter((Venue.city.ilike('%' + searched_term + '%') |
                                    Venue.name.ilike('%' + searched_term + '%') |
                                    Venue.state.ilike('%' + searched_term + '%') |
                                    Venue.genres.ilike('%' + searched_term + '%'))))
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.get(venue_id)
    upcoming_shows = Show.query.join(Venue).filter(Venue.id == venue_id).filter(Show.show_time > datetime.utcnow())
    past_shows = Show.query.join(Venue).filter(Venue.id == venue_id).filter(Show.show_time <= datetime.utcnow())
    return render_template('pages/show_venue.html', venue=data, upcoming_shows=upcoming_shows, past_shows=past_shows)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    if form.validate():
        add = request.form.get  # to avoid repetition
        genres = ' '.join(form.genres.data)  # converts the list of genres to a str ing before storing it
        # check database if area exist, else create a new area using the city and state and link it to the venue
        area = Area.query.filter_by(city=add('city'), state=add('state')).first()
        if not area:
            area = Area(city=add('city'), state=add('state'))
            db.session.add(area)
            db.session.commit()
        try:
            new_venue = Venue(name=add('name'), city=add('city'), state=add('state'), address=add('address'),
                              phone=add('phone'), genres=genres, website_link=add('website_link'),
                              facebook_link=add('facebook_link'),
                              looking_for_talent=form.seeking_talent.data,
                              seeking_description=add('seeking_description'),
                              area=area.id)

            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
        except:
            db.session.rollback()
            flash('An error occurred. Venue ' + add('name') + ' could not be listed.')
        return redirect(url_for('index'))
    else:
        print(form.form_errors)
        flash('An error occurred with the form')
        return redirect(url_for('index'))


@app.route('/venues/delete/<venue_id>')
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue {venue.name} has been deleted')
        return redirect(url_for('index'))
    except:
        db.session.rollback()
        flash(f'Venue {venue.name} could not be deleted')
        return redirect(url_for('index'))

    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    searched_term = request.form.get('search_term')
    response = (Artist.query.filter((Artist.city.ilike('%' + searched_term + '%') |
                                     Artist.name.ilike('%' + searched_term + '%') |
                                     Artist.state.ilike('%' + searched_term + '%') |
                                     Artist.genres.ilike('%' + searched_term + '%'))))
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    upcoming_shows = Show.query.join(Artist).filter(Artist.id == artist_id).filter(Show.show_time > datetime.utcnow())
    past_shows = Show.query.join(Artist).filter(Artist.id == artist_id).filter(Show.show_time <= datetime.utcnow())
    return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows,
                           past_shows=past_shows)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm()
    form.name.data = artist.name
    form.genres.data = artist.genres.split()
    form.state.data = artist.state
    form.city.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.looking_for_venues
    form.seeking_description.data = artist.seeking_description
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    if form.validate():
        artist.name = form.name.data
        artist.phone = form.phone.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.genres = ' '.join(form.genres.data)
        artist.image_link = form.image_link.data
        artist.website_link = form.website_link.data
        artist.looking_for_venues = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        flash(f'An error occurred, Please check form and try again')
        return redirect(url_for('show_artist', artist_id=artist_id))

    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name
    form.genres.data = venue.genres.split()
    form.state.data = venue.state
    form.address.data = venue.address
    form.city.data = venue.city
    form.phone.data = venue.phone
    form.seeking_talent.data = venue.looking_for_talent
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website_link
    form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)

    # TODO: populate form with values from venue with ID <venue_id>


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)
    if form.validate():
        venue.name = form.name.data
        venue.phone = form.phone.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.genres = ' '.join(form.genres.data)
        venue.image_link = form.image_link.data
        venue.website_link = form.website_link.data
        venue.looking_for_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        db.session.commit()
        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        flash(f'Check submission and try again')
        return redirect(url_for('show_venue', venue_id=venue_id))

    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    add = request.form.get
    form = ArtistForm(request.form)
    if form.validate():
        try:
            genres = ' '.join(form.genres.data)  # converts the list of genres before storing

            new_artist = Artist(name=add('name'), city=add('city'), state=add('state'),
                                phone=add('phone'), genres=genres, website_link=add('website_link'),
                                facebook_link=add('facebook_link'), image_link=add('image_link'),
                                looking_for_venues=add('seeking_venue'), seeking_description=add('seeking_description'))
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist' + request.form['name'] + ' was successfully listed!')
        except:
            db.session.rollback()
            flash('An error occurred. Artist ' + add('name') + ' could not be listed.')
        return redirect(url_for('index'))
    else:
        flash(f'An error occurred, Please check form and try again')
        return redirect(url_for('index'))

    #  Shows


#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at shows
    # TODO: replace with real venues data.
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)
    if form.validate():
        try:
            artist_id = request.form.get('artist_id')
            venue_id = request.form.get('venue_id')
            artist = Artist.query.get(artist_id)
            venue_name = Venue.query.get(venue_id).name
            show = Show(artist_id=artist.id, venue_id=venue_id,
                        show_time=request.form.get('start_time'))
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Show could not be listed, Check submission and try again!')
            return redirect(url_for('index'))
    else:
        flash('An error occurred, check the form and try again')
        return redirect(url_for('index'))


@app.shell_context_processor
def shell():
    return {'db': db, 'venues': Venue, 'artists': Artist, 'areas': Area, 'show': Show}


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
