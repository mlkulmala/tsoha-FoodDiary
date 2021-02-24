from app import app
from flask import redirect, render_template, request, session
import users, foodstuffs, fooddiaries, utils

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/food_search")
def search():
    user_id = users.user_id()
    portions = fooddiaries.get_todays_diary(user_id)
    total_calories = fooddiaries.get_total_calories(user_id)
    return render_template("food_search.html", portions=portions, total_calories=total_calories)

@app.route("/select_food", methods=["GET"])
def select_food():
    food_name = request.args["searched_food"]
    food_list = foodstuffs.get_foodstuff_by_name(food_name)
    meals = utils.get_meals()
    return render_template("select_food.html", food_name=food_name, foodstuffs=food_list, meals=meals)

@app.route("/diary_entry", methods=["GET"])
def diary_entry():
    user_id = users.user_id()
    if request.args:
        foodstuff_id = request.args["foodstuff"]
        meal_id = utils.get_meal_id(request.args["meal"])
        amount = request.args["amount"]
        if fooddiaries.add_to_diary(user_id, foodstuff_id, meal_id, amount):
            return redirect("/food_search")
        else:
            return render_template("error.html", message="Lisäys ruokapäiväkirjaan ei onnistunut.")
    return render_template("error.html", message="Tarkista, että teit kaikki valinnat.")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        if users.login(username, password):
            return render_template("food_search.html")
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
            return redirect("/create_profile")
        else:
            return render_template("error.html", message="Tunnuksen luominen ei onnistunut")

@app.route("/create_profile")
def create_profile():
    return render_template("personal_details.html")

@app.route("/add_details", methods=["GET"])
def add_details():
    user_id = users.user_id()
    if request.args:
        gender_id = request.args["gender"]
        gender = users.get_gender(gender_id)
        age = request.args["age"]
        height = request.args["height"]
        weight = request.args["weight"]
        activity = request.args["activity"]
        if users.add_personal_details(user_id, gender_id, age, height, weight, activity):
            return redirect("/profile/"+str(user_id))
        else:
            return render_template("error.html", message="Tietojen lisääminen ei onnistunut")
    return render_template("personal_details.html")

@app.route("/profile/<int:id>")
def profile(id):
    details = users.personal_details(id)
    return render_template("profile.html", details=details)
