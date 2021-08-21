from flask import Flask, render_template, request, session, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

dburl = "sqlite:///" + os.getcwd() + "/cuentas_usuarios.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dburl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nombre = db.Column(db.String)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/consultar")
def consultar():
    nickname = request.args.get("nickname")
    usuario = Users.query.filter_by(username=nickname).first()

    if usuario:
        mns = f"<h1>Usuario encontrado: {usuario.username} </h1>"
        return mns

    mns =  f"<h1>Este usuario {nickname} no existe, simplepage: Devuelva manualmente...</h1>"
    return mns



@app.route("/registrar", methods=["GET", "POST"])
def registrar():

    if request.method == "POST":
        usuarioxx = request.form["username"]

        xxx = Users.query.filter_by(username=usuarioxx).first()
        if xxx:
            return render_template("signup.html")
        else:
            seguridad_password = generate_password_hash(request.form["password"], method="sha256")
            nuevo_usuario_creator = Users(username=request.form["username"], password=seguridad_password, nombre = request.form["nombre"])
            db.session.add(nuevo_usuario_creator)
            db.session.commit()
            mns = f"<h1>Te has registrado con éxito, bienvenid@</h1>"
            return mns

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nuevo_usuario_creator = Users.query.filter_by(username=request.form["username"]).first()

        if nuevo_usuario_creator and check_password_hash(nuevo_usuario_creator.password, request.form["password"]):
            session["username"] = nuevo_usuario_creator.username
            return "<h1>HAS INICIADO SESION BIENVENID@</h1>"
        return "<h1>Este usuario no existe.</h1>"
    return render_template("login.html")

@app.route("/home")
def home():
    if "username" in session:
        return "<h1>Estas logeado</h1>"

    return "<h1>Necesitas iniciar sesion primero.</h1>"

@app.route("/logout")
def logout():
    session.pop("username", None)

    return "Has cerrado sesión"

app.secret_key = "asdf"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=2889)
