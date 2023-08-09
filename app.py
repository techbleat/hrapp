from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import traceback
import os
import datetime

app = Flask(__name__)
version = "1.7.1"

user = os.environ.get("POSTGRES_USER")
pw = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
db = os.environ.get("POSTGRES_DATABASE_NAME")
DB_URL = f"postgresql+psycopg2://{user}:{pw}@{host}/{db}"
print(DB_URL)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, unique=True, nullable=False)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    city = db.Column(db.String)
    

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/')
def index():
    user = User.query.all() 
    return render_template('index.html', user=user, gmt_dt=datetime.datetime.utcnow())

@app.route("/user", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            firstname=request.form["firstname"],
            lastname=request.form["lastname"],
            email=request.form["email"],
            password=request.form["password"],
            city=request.form["city"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = User.query.filter_by(id=id).all()
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))
