#!/bin/python
from flask import Flask, render_template, request, redirect, session
import bdd
import sqlite3
import secrets
from password import check_password

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(50)
cursor_bdd, connexion_bdd = bdd.get_cursor_and_connexion()
error = False

def check_connected(destination):
    if("pass" not in session and "user" not in session):
        return render_template("login.html")
    return destination

@app.route('/')
def home():
    try:
        tab = bdd.get_passwords(cursor_bdd, session["pass"], session["user"])
        return render_template("home.html", tab=tab)
    except:
        return render_template("login.html")


@app.route('/add_new', methods=["GET"])
def add_new():
    return check_connected(render_template("add_password.html"))

@app.route("/remove_pass", methods=["GET"])
def remove_pass():
    if("pass" in session and "user" in session) and check_password(session["pass"],bdd.get_user_password_hash(cursor_bdd,session["user"])):
        try:
            id = request.args.get("id")
            bdd.delete_password(cursor_bdd, connexion_bdd, id)
        except:
            pass
    return redirect("/")


@app.route("/valid_add_new",  methods=["POST"])
def valid_add_new():
    if("pass" not in session and "user" not in session):
        return render_template("login.html")
    password_name = request.form.get("name")
    password_value = request.form.get("value")
    bdd.add_password(cursor_bdd, connexion_bdd, password_name, password_value, session["pass"], session["user"])
    return redirect("/")

@app.route("/login")
def login():
    global error
    if error:
        return render_template("login.html", error=True)
        error = False
    else:
        return render_template("login.html")

@app.route("/valid_login",  methods=["POST"])
def valid_login():
    global error
    password = request.form.get("password")
    user_name = request.form.get("name")
    hash_ = bdd.get_user_password_hash(cursor_bdd, user_name)
    if(check_password(password, hash_)):
        session["pass"]=password
        session["user"]=user_name
        return redirect("/")
    else:
        error = True
        return redirect("/login")

if __name__ == "__main__":
    app.run()