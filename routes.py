from app import app
from flask import redirect, render_template, request
import users, foodstuffs

@app.route("/")
def index():
    if request.args:
        meal = request.args["meal"]
        foodstuff = request.args["foodstuff"]
        amount = request.args["amount"]
    else:
        selected_foodstuffs = []
    selected_foodstuffs = []
    selected_foodstuffs = foodstuffs.get_foodstuffs()
    return render_template("index.html", foodstuffs=selected_foodstuffs) 

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Tunnuksen luominen ei onnistunut")

