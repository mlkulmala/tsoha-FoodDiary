from db import db

def get_meals():
    sql = "SELECT * FROM meals"
    meals = db.session.execute(sql).fetchall()
    return meals

def get_meal_id(meal_name):
    sql = "SELECT id FROM meals WHERE name=:meal_name"
    result = db.session.execute(sql, {"meal_name":meal_name})
    meal_id = result.fetchone()[0]
    return meal_id

def add_personal_details(user_id, gender_id, age, height, weight, activity):
    sql = "INSERT INTO personal_details (user_id, gender_id, age, height, weight, activity) " \
        "VALUES (:user_id, :gender_id, :age, :height, :weight, :activity)"
    result = db.session.execute(sql, {"user_id":user_id, "gender_id":gender_id, "age":age, \
        "height":height, "weight":weight, "activity":activity})
    db.session.commit()
    return True

def get_gender(gender_id):
    sql = "SELECT gender FROM gender WHERE id=:gender_id"
    result = db.session.execute(sql, {"gender_id":gender_id})
    gender = result.fetchone()[0]
    return gender

def count_energy_consumption(gender_id, age, height, weight, activity):
    if gender_id == 1:
        consumption = activity * (447.593 + (9.247 * weight) + (3.098 * height) - (4.33 * age))
    else:
        consumption = activity * (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
    return consumption
