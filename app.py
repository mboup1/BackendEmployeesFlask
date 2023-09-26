from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='./template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle SQLAlchemy
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return f"Todo : {self.name} {self.firstName} {self.email}"

# Ajouter une tâche
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        firstName = request.form['firstName']
        name = request.form['name']
        email = request.form['email']
        new_person = Person(name=name, firstName=firstName, email=email)
        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produite lors de la sauvegarde"
    else:
        persons = Person.query.order_by(Person.created_at)
    return render_template("index.html", persons=persons)

# Mettre à jour une tâche
@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    person = Person.query.get_or_404(id)
    if request.method == "POST":
        person.firstName = request.form["firstName"]
        person.name = request.form["name"]
        person.email = request.form["email"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Nous ne pouvons pas modifier les"
    else:
        title = "Mise à jour"
        return render_template("update.html", title=title, person=person)

# Suprrimer une tâche
@app.route("/delete/<int:id>/")
def delete(id):
    person = Person.query.get_or_404(id)
    try:
        db.session.delete(person)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Une erreur s'est produite"

# A propos de ...
@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/addform/')
def addform():
    return render_template("addform.html")

@app.route('/add-person/<name>/<firstName>/<email>/', methods=['GET'])
def add_person(name, firstName, email):
    new_person = Person(name=name, firstName=firstName, email=email)
    db.session.add(new_person)
    db.session.commit()
    return f'Person: {firstName} {name} {email} has been created successfully!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


