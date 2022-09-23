from flask import Blueprint, render_template, request, flash, redirect
from .models import Animal
from . import db
from .images import get_images_from_google, wd

views = Blueprint('views', __name__)


@views.route('/', methods=["POST", "GET"])
def index():
    pictures = []
    if request.method == "POST":
        favorite = request.form.get('animal') or None
        if Animal.find_by_name(favorite.strip()) is not None or Animal.find_by_name(favorite.lower()) is not None:
            flash("You fool! You already added that animal!")
        else:
            if len(favorite) < 3:
                flash("You brute! The animal name is too short!", category='error')
            elif any(char.isdigit() for char in favorite) == True:
                flash("You jerk! That's not an animal, that's a number!")
            else:
                new_animal = Animal(name=favorite)
                db.session.add(new_animal)
                db.session.commit()
                flash(
                    'You lovely humanbeing! Your animal has been added to the database!', category='success')
                pictures.append(get_images_from_google(wd, 1))
                for url in pictures:
                    print(url)
                return redirect('/')

    return render_template('index.html', pictures=pictures)


@views.route('/results', methods=["POST", "GET"])
def results():
    animals = Animal.query.order_by(Animal.created).all()
    return render_template('results.html', animals=animals, )


@views.route('/delete/<int:id>')
def delete(id):
    animal_to_delete = Animal.query.get_or_404(id)
    try:
        db.session.delete(animal_to_delete)
        db.session.commit()
        return redirect('/results')
    except:
        return "We couldn't delete your animal"


@views.route('/modal')
def modal():
    return render_template('/modal')


@views.route('/delete_all')
def delete_all():
    try:
        db.session.query(Animal).delete()
        db.session.commit()
        return redirect('/results')
    except:
        return "We couldn't delete your animal"
