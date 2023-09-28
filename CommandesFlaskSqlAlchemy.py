# python -m venv myenv - myenv\Scripts\Activate - pip install Flask

from app import app, db, Task

with app.app_context():
    new_task = Task( name="Mboup", firstName="Dame", email="Email")
    db.session.add(new_task)
    db.session.commit()


with app.app_context():
    db.drop_all()


# CREATE DATABASE IF NOT EXISTS flask
#         CHARACTER SET utf8 COLLATE utf8_general_ci


# CREATE TABLE flask (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     firstname VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
#     name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci,
#     email VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci
# );