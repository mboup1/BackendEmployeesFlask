from app import app, db, Task

with app.app_context():
    new_task = Task( name="Mboup", firstName="Dame", email="Email")
    db.session.add(new_task)
    db.session.commit()


with app.app_context():
    db.drop_all()