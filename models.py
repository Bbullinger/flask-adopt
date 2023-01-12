from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, URL, Optional, NumberRange

db = SQLAlchemy()


# def create_app():
#     app = Flask(__name__)

#     app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adoption"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["SECRET_KEY"] = "my_password"
#     return app


# def connect_db(app):

#     db = SQLAlchemy(app)
#     db.app = app
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()
#     return db
def connect_db(app):
    db.app = app
    db.init_app(app)


accepted_species = ["cat", "dog", "porcupine"]


class Pet(db.Model):
    """Pet"""

    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"id {self.id}, name {self.name}, species {self.species}, photo_url {self.photo_url}, age {self.age}, notes {self.notes}, available {self.available}"

    def image(self):
        if self.photo_url:
            return self.photo_url
        else:
            return "https://thumbs.dreamstime.com/b/vector-flat-cartoon-illustration-icon-design-adopt-me-dont-buy-dog-cat-pet-adoption-puppy-pooch-kitty-cat-looking-up-to-red-heart-99463424.jpg"


class PetForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    species = SelectField(
        "Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")]
    )
    photo_url = StringField("Photo URL", validators=[URL(), Optional()])
    age = IntegerField("Age", validators=[NumberRange(0, 30)])
    notes = StringField("Notes")
    available = BooleanField("Available", validators=[InputRequired()])


class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[URL(), Optional()])
    notes = StringField("Notes")
    available = BooleanField("Available", validators=[InputRequired()])
