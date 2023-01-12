from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, PetForm, EditPetForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adoption"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my_password"


# toolbar = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()


# app = create_app()
# db = connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/")
def home_page():

    pets = Pet.query.all()

    return render_template("index.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.data["name"],
            species=form.data["species"],
            photo_url=form.data["photo_url"],
            age=form.data["age"],
            notes=form.data["notes"],
            available=form.data["available"],
        )
        flash(f"added {new_pet.name}")
        db.session.add(new_pet)
        db.session.commit()

        return redirect("/")
    else:
        print(form.data["name"])
        return render_template("add_pet.html", form=form)


# @app.route("/<int:pet_id>")
# def show_pet(pet_id):
#     pet = Pet.query.get_or_404(pet_id)
#     return render_template("show_pet.html", pet=pet)


@app.route("/<int:pet_id>/", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect("/")
    else:
        return render_template("show_pet.html", pet=pet, form=form)
