from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL 

app = Flask(__name__, template_folder='./template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'


mysql = MySQL(app)

# Ajouter une personne
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        firstName = request.form['firstName']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS flask_array (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
                name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
                email VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci
            );''')
        cur.execute("INSERT INTO flask_array (firstName, name, email) VALUES (%s, %s, %s)", (firstName, name, email))
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    else:
        cur = mysql.connection.cursor()
        personsIndex = cur.execute("SELECT * FROM flask_array")
        personsIndex = cur.fetchall()
        cur.close()
        personsIndex = [dict(id=row[0], firstName=row[1], name=row[2], email=row[3], created_at=row[4]) for row in personsIndex]
    return render_template("index.html", personsIndex=personsIndex)

# Mettre à jour une personne
@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        firstName = request.form['firstName']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE flask_array SET firstName = %s, name = %s, email = %s WHERE id = %s",
            (firstName, name, email, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    #Bloc else (Lorsque la requête est une requête GET) :
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM flask_array WHERE id = %s", (id,))
        person = cur.fetchone()
        cur.close()
        if person is None:
            return "Record not found", 404
        person_dict = dict(id=person[0], firstName=person[1], name=person[2], email=person[3], created_at=person[4])
        return render_template("update.html", person=person_dict)

# Suprrimer une personne
@app.route("/delete/<int:id>/", methods=["GET", "POST"])
def delete(id):
    cur = mysql.connection.cursor()
    #Partie optionnelle qui permet de passer le prénom et le nom du la personne concernée à delete_confirmation.html
    cur.execute("SELECT * FROM flask_array WHERE id = %s", (id,))
    person = cur.fetchone()
    cur.close()

    if person is None:
        return "Record not found", 404

    person_dict = dict(id=person[0], firstName=person[1], name=person[2], email=person[3], created_at=person[4])

    if request.method == "POST":
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM flask_array WHERE id = %s', [id])
            mysql.connection.commit()
            cur.close()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produite"
    else:
        return render_template("delete_confirmation.html", person=person_dict)



# A propos de ...
@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/add/')
def addForm():
    return render_template("addForm.html")

if __name__ == '__main__':
    app.run(debug=True)


# def init_db():
#     cur = mysql.connection.cursor()
#     # cur.execute('''
#     #     CREATE DATABASE IF NOT EXISTS flask 
#     #     CHARACTER SET utf8 COLLATE utf8_general_ci;
#     #     ''')
#     # cur.execute("USE flask;")
#     # cur.execute('''CREATE TABLE IF NOT EXISTS flask_array (
#     #             id INT AUTO_INCREMENT PRIMARY KEY,
#     #             firstname VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
#     #             name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
#     #             email VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci
#     #         );''')
#     mysql.connection.commit()
#     cur.close()