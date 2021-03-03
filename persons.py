from db import db
from flask import session
import re




def get_personal_details(user_id):
    sql = "SELECT gender, age, height, weight, activity FROM personal_details " \
        "JOIN users ON users.id = personal_details.user_id " \
        "JOIN gender ON gender.id = personal_details.gender_id " \
        "WHERE users.id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def add_personal_details(user_id, gender_id, age, height, weight, activity):
    sql = "INSERT INTO personal_details (user_id, gender_id, age, height, weight, activity) " \
        "VALUES (:user_id, :gender_id, :age, :height, :weight, :activity)"
    result = db.session.execute(sql, {"user_id":user_id, "gender_id":gender_id, "age":age, \
        "height":height, "weight":weight, "activity":activity})
    db.session.commit()
    return True

def update_personal_details(user_id, gender_id, age, height, weight, activity):
    sql = "UPDATE personal_details SET gender_id=:gender_id, age=:age, height=:height, weight=:weight, " \
        "activity=:activity WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id, "gender_id":gender_id, "age":age, \
        "height":height, "weight":weight, "activity":activity})
    db.session.commit()
    return True


def get_gender(gender_id):
    sql = "SELECT gender FROM gender WHERE id=:gender_id"
    result = db.session.execute(sql, {"gender_id":gender_id})
    gender = result.fetchone()[0]
    return gender

def add_calorie_goal(user_id, gender_id, age, height, weight, activity):
    if gender_id == 1:
        calorie_goal = round(float(activity) * (447.593 + (9.247 * float(weight)) + \
            (3.098 * float(height)) - (4.33 * float(age))))
    else:
        calorie_goal = round(float(activity) * (88.362 + (13.397 * float(weight)) + \
            (4.799 * float(height)) - (5.677 * float(age))))
    sql = "UPDATE personal_details SET calorie_goal=:calorie_goal WHERE user_id=:user_id"
    result = db.session.execute(sql, {"calorie_goal":calorie_goal, "user_id":user_id})
    db.session.commit()
    return True

def get_calorie_goal(user_id):
    sql = "SELECT calorie_goal FROM personal_details WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    calorie_goal = result.fetchone()
    if (calorie_goal == None):
        return 2000
    return calorie_goal[0]

def set_calorie_goal(user_id, goal):
    sql = "UPDATE personal_details SET calorie_goal=:calorie_goal WHERE user_id=:user_id"
    result = db.session.execute(sql, {"calorie_goal":goal})
    db.session.commit()
    return True


