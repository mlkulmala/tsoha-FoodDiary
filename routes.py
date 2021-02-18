from app import app
from flask import redirect, render_template, request
import users, foodstuffs

@app.route("/", methods=["GET"])
def index():
    meal = None
    food = None
    amount = None
    diary_portions = []
    error = None
    if request.args:
        meal = request.args["meal"]
        food = request.args["food_search"]
        amount = request.args["amount"]
    else:
        error = "Tietoja puuttuu"
    return render_template("index.html", meal=meal, food=food, amount=amount, error=error) 

@app.route("/food_search", methods=["GET"])
def search():
    food_name = request.args["food_search"]
    foodlist = foodstuffs.get_foodstuff_by_name(food_name)
    # foodlist = foodstuffs.get_foodstuffs()
    # jos tuloksia yli 10, pyydä tarkentamaan hakua
    return render_template("food_search.html", food_name=food_name, foodstuffs=foodlist)

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

