from app import app
from flask import redirect, render_template, request, session
from datetime import datetime
import users, foodstuffs, fooddiaries, utils

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/food_search")
def search():
    user_id = users.user_id()
    portions = fooddiaries.get_todays_diary(user_id)
    current_date = datetime.today().strftime('%Y-%m-%d')
    total = fooddiaries.get_calories_and_nutrients(user_id, current_date)
    kcal = total[0]
    fat = total[1]
    carbs = total[2]
    pro = total[3]
    fiber = total[4]
    calorie_goal = users.get_calorie_goal(user_id)
    kcal_left = calorie_goal - kcal
    return render_template("food_search.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber, kcal_left=kcal_left)


@app.route("/select_food", methods=["GET"])
def select_food():
    food_name = request.args["searched_food"]
    food_list = foodstuffs.get_foodstuff_by_name(food_name)
    meals = utils.get_meals()
    return render_template("select_food.html", food_name=food_name, foodstuffs=food_list, meals=meals)

@app.route("/diary_entry", methods=["POST"])
def diary_entry():
    user_id = users.user_id()
    if request.form:
        foodstuff_id = request.form["foodstuff"]
        meal_id = utils.get_meal_id(request.form["meal"])
        amount = request.form["amount"]
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
            return redirect("/food_search")
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
        password_val = request.form["validate_password"]
        if len(username) < 4:
            return render_template("register.html", error=True, message="Tunnuksessa pitää olla vähintään neljä merkkiä.")
        if not users.password_qualified(password):
            return render_template("register.html", error=True, message="Salasana ei täytä kriteerejä.")
        if (password != password_val):
            return render_template("register.html", error=True, message="Salasanat eivät täsmää.")
        if users.register(username, password):
            return redirect("/create_profile")
        else:
            return render_template("register.html", error=True, message="Tunnuksen luominen ei onnistunut.")

@app.route("/create_profile")
def create_profile():
    return render_template("personal_details.html")

@app.route("/add_details", methods=["POST"])
def add_details():
    user_id = users.user_id()
    if request.form:
        gender_id = request.form["gender"]
        gender = users.get_gender(gender_id)
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        activity = request.form["activity"]
        users.add_calorie_goal(user_id, gender_id, age, height, weight, activity)
        if users.has_profile(user_id):
            if users.update_personal_details(user_id, gender_id, age, height, weight, activity):
                return redirect("/profile/"+str(user_id))
        if users.add_personal_details(user_id, gender_id, age, height, weight, activity):
            return redirect("/profile/"+str(user_id))
        else:
            return render_template("error.html", message="Tietojen lisääminen ei onnistunut")
    return render_template("personal_details.html")

@app.route("/profile/<int:id>")
def profile(id):
    details = users.personal_details(id)
    calorie_goal = users.get_calorie_goal(id)
    return render_template("profile.html", details=details, calorie_goal=calorie_goal)

@app.route("/diary_days", methods=["GET"])
def diary_days():
    user_id = users.user_id()
    if request.args:
        date = request.args["diary_date"]
    else:
        date = datetime.today().strftime('%Y-%m-%d')
    # date = datetime.today().strftime('%Y-%m-%d')
    total = fooddiaries.get_calories_and_nutrients(user_id, date)
    kcal = total[0]
    fat = total[1]
    carbs = total[2]
    pro = total[3]
    fiber = total[4]
    calorie_goal = users.get_calorie_goal(user_id)
    portions = fooddiaries.get_diary_by_date(user_id, date)
    return render_template("diary_days.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber)

@app.route("/get_diaries", methods=["POST"])
def get_diaries():
    user_id = users.user_id()
    date = request.form["diary_date"]
    total = fooddiaries.get_calories_and_nutrients(user_id, date)
    kcal = total[0]
    fat = total[1]
    carbs = total[2]
    pro = total[3]
    fiber = total[4]
    calorie_goal = users.get_calorie_goal(user_id)
    portions = fooddiaries.get_diary_by_date(user_id, date)
    return render_template("diary_days.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber)

