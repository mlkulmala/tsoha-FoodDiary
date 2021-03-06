from app import app
from flask import redirect, render_template, request, session
from datetime import datetime
import foodstuffs, fooddiaries, persons, users, utils



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        if users.login(username, password):
            return redirect("/food_search")
        else:
            return render_template("login.html", error=True, message="Väärä tunnus tai salasana")

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
    calorie_goal = fooddiaries.get_todays_goal(user_id)
    kcal_left = calorie_goal - kcal
    return render_template("food_search.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber, kcal_left=kcal_left)


@app.route("/select_food", methods=["GET"])
def select_food():
    user_id = users.user_id()
    food_name = request.args["searched_food"]
    food_list = foodstuffs.get_foodstuff_by_name(food_name, user_id)
    meals = utils.get_meals()
    return render_template("select_food.html", food_name=food_name, foodstuffs=food_list, meals=meals)

@app.route("/diary_entry", methods=["POST"])
def diary_entry():
    user_id = users.user_id()
    if (session["csrf_token"] != request.form["csrf_token"]):
        return abort(403)
    if request.form["foodstuff"]:
        foodstuff_id = request.form["foodstuff"]
        meal_id = utils.get_meal_id(request.form["meal"])
        amount = request.form["amount"]
        if fooddiaries.add_to_diary(user_id, foodstuff_id, meal_id, amount):
            return redirect("/food_search")
        else:
            return render_template("error.html", message="Lisäys ruokapäiväkirjaan ei onnistunut.")
    return render_template("error.html", message="Tarkista, että teit kaikki valinnat.")

@app.route("/create_profile")
def create_profile():
    user_id = users.user_id()
    goal = persons.get_personal_goal(user_id)
    details = persons.get_personal_details(user_id)
    return render_template("personal_details.html", goal=goal, details=details)

@app.route("/add_details", methods=["POST"])
def add_details():
    user_id = users.user_id()
    if request.form:
        if (session["csrf_token"] != request.form["csrf_token"]):
            return abort(403)
        gender_id = request.form["gender"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        activity = request.form["activity"]
        if persons.add_personal_details(user_id, gender_id, age, height, weight, activity) \
            and persons.set_goal_priority(user_id, False):
            return redirect("/profile/"+str(user_id))
        else:
            return render_template("error.html", message="Tietojen lisääminen ei onnistunut.")
    return render_template("personal_details.html")

@app.route("/add_goal", methods=["POST"])
def add_goal():
    user_id = users.user_id()
    if (session["csrf_token"] != request.form["csrf_token"]):
        return abort(403)
    personal_goal = request.form["goal"]
    if persons.add_personal_goal(user_id, personal_goal) and persons.set_goal_priority(user_id, True):
        return redirect("/profile/"+str(user_id))
    else:
        return render_template("error.html", message="Tavoitteen lisääminen ei onnistunut.")


@app.route("/profile/<int:id>")
def profile(id):
    user_id = users.user_id()
    details = persons.get_personal_details(id)
    goal_priority = persons.get_goal_priority(id)
    personal_goal = persons.get_personal_goal(user_id)
    if not goal_priority:
        priority = False
    else:
        priority = True
    calorie_goal = persons.count_calorie_goal_by_id(id)
    return render_template("profile.html", details=details, personal_goal=personal_goal, \
        calorie_goal=calorie_goal, priority=priority)

@app.route("/diary_days", methods=["GET"])
def diary_days():
    user_id = users.user_id()
    if request.args:
        date = request.args["diary_date"]
    else:
        date = datetime.today().strftime('%Y-%m-%d')
    total = fooddiaries.get_calories_and_nutrients(user_id, date)
    kcal = total[0]
    fat = total[1]
    carbs = total[2]
    pro = total[3]
    fiber = total[4]
    portions = fooddiaries.get_diary_by_date(user_id, date)
    calorie_goal = fooddiaries.get_calorie_goal_by_date(user_id, date)
    return render_template("diary_days.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber, date=date)

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
    portions = fooddiaries.get_diary_by_date(user_id, date)
    calorie_goal = portions[9]
    return render_template("diary_days.html", portions=portions, calorie_goal=calorie_goal, \
         kcal=kcal, fat=fat, carbs=carbs, pro=pro, fiber=fiber)

@app.route("/remove_from_diary", methods=["GET"])
def remove_from_diary():
    portion_id = request.args["remove"]
    selected = fooddiaries.get_portion(portion_id)
    meal= selected[0]
    name = selected[1]
    amount = selected[2]
    return render_template("remove.html", meal=meal, name=name, amount=amount, portion_id=portion_id)

@app.route("/delete", methods=["GET"])
def delete():
    portion_id = request.args["portion_id"]
    portion_deleted = fooddiaries.delete_portion(portion_id)
    if portion_deleted:
        return redirect("/food_search")
    else:
        return render_template("error.html", message="Päiväkirjamerkinnän poisto ei onnistunut.")

@app.route("/new_foodstuff")
def new_foodstuff():
    return render_template("new_foodstuff.html")

@app.route("/add_foodstuff", methods=["POST"])
def add_foodstuff():
    user_id = users.user_id()
    name = request.form["name"]
    kcal = request.form["kcal"]
    fat = request.form["fat"]
    carbs = request.form["fat"]
    pro = request.form["pro"]
    fiber = request.form["fiber"]
    if foodstuffs.add_foodstuff(name, kcal, fat, carbs, pro, fiber, user_id):
        return render_template("foodstuff_added.html", name=name, error=False)
    else:
        return render_template("foodstuff_added.html", name=name, error=True, message="Tietojen tallentaminen ei onnistunut.")
