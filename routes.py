from app import app 
from flask import redirect, render_template, request 
import users, foodstuffs, fooddiaries

@app.route("/")
def index():
    user_id = users.user_id()
    portions = []
    foodstuff = None
    meal = None
    amount = None
    if request.args:
        foodstuff = request.args["foodstuff"]
        meal = request.args["meal"]
        amount = request.args["amount"]
        if user_id != 0:
            portions = fooddiaries.add_to_diary(user_id, foodstuff, meal, amount)
    return render_template("index.html", foodstuff=foodstuff, meal=meal, amount=amount, portions=portions)


@app.route("/select_food", methods=["GET"])
def select_food():
    food_name = request.args["searched_food"]
    foodlist = foodstuffs.get_foodstuff_by_name(food_name)
    return render_template("select_food.html", food_name=food_name, foodstuffs=foodlist)

@app.route("/add_portion", methods=["GET"])
def add_portion():
    user_id = users.user_id()
    if user_id != 0:
        fooddiaries.add_to_diary(user_id, date, foodstuff, meal, amount)
    return redirect("/")



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

