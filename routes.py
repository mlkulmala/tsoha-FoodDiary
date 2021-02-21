from app import app 
from flask import redirect, render_template, request 
import users, foodstuffs, fooddiaries, utils

@app.route("/", methods=["GET"])
def index():
    user_id = users.user_id()
    portions = []
    if user_id != 0:
        portions = fooddiaries.get_todays_diary(user_id)
        if request.args:
            foodstuff_id = request.args["foodstuff"]
            meal_id = utils.get_meal_id(request.args["meal"])
            amount = request.args["amount"]
            fooddiaries.add_to_diary(user_id, foodstuff_id, meal_id, amount)
    return render_template("index.html", portions=portions)


@app.route("/select_food", methods=["GET"])
def select_food():
    food_name = request.args["searched_food"]
    foodlist = foodstuffs.get_foodstuff_by_name(food_name)
    meals = utils.get_meals()
    return render_template("select_food.html", food_name=food_name, foodstuffs=foodlist, meals=meals)



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

