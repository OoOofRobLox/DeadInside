from flask_login import UserMixin

from app import db, DEFAULT_PROFILE_IMAGE

genre_movie = db.Table('genre_movie',
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
                       )

criteria_movie = db.Table('criteria_movie',
                          db.Column('criteria_id', db.Integer, db.ForeignKey('criteria.id'), primary_key=True),
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
                          )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    src = db.Column(db.String(1023), unique=False, nullable=False, default=DEFAULT_PROFILE_IMAGE)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)

    library = db.relationship('Library', backref='user', lazy=True)
    comments = db.relationship('Commentary', backref='user', lazy=True)


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    countries = db.relationship('Country', backref='city', lazy=True)


class Country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    users = db.relationship('User', backref='country', lazy=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)


class Library(db.Model):
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True)
    # movies = db.column(db.)

    users = db.relationship('User', uselist=False, backref='library', lazy=True)


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    generalRating = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    isFavorite = db.Column(db.Boolean, unique=False, nullable=False)

    genres = db.relationship('Genre', secondary=genre_movie, lazy=False, backref=db.backref('genres', lazy=True))
    criterias = db.relationship('Criteria', secondary=criteria_movie, lazy=False,
                                backref=db.backref('criterias', lazy=True))
    comments = db.relationship('Commentary', backref='movie', lazy=True)


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    movies = db.relationship('Movie', secondary=genre_movie, lazy=False, backref=db.backref('movies', lazy=True))


class Criteria(db.Model):
    __tablename__ = "criteria"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    evaluation = db.Column(db.Integer, unique=False, nullable=False)

    movies = db.relationship('Movie', secondary=criteria_movie, lazy=False, backref=db.backref('movies', lazy=True))


class Commentary(db.Model):
    __tablename__ = "commentary"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(511), unique=False, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
