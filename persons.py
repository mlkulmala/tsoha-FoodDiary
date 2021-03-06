from db import db
from flask import session
import fooddiaries



def get_personal_details(user_id):
    sql = "SELECT gender, age, height, weight, activity FROM personal_details " \
        "JOIN users ON users.id = personal_details.user_id " \
        "JOIN gender ON gender.id = personal_details.gender_id " \
        "WHERE users.id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def get_personal_goal(user_id):
    sql = "SELECT personal_goal FROM personal_details WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if result == None:
        return None
    else:
        return result[0]

def get_goal_priority(user_id):
    sql = "SELECT goal_priority FROM personal_details WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if result == None:
        return None
    else:
        return result[0]

def set_goal_priority(user_id, priority):
    sql = "UPDATE personal_details SET goal_priority=:goal_priority WHERE user_id=:user_id"
    db.session.execute(sql, {"user_id":user_id, "goal_priority":priority })
    db.session.commit()
    return True

def add_personal_goal(user_id, goal):
    if has_profile(user_id):
        update_personal_goal(user_id, goal)
    else:
        sql = "INSERT INTO personal_details (user_id, personal_goal) VALUES (:user_id, :personal_goal)"
        db.session.execute(sql, {"user_id":user_id, "personal_goal":goal})
        db.session.commit()
    fooddiaries.update_todays_goal(user_id, goal)
    return True

def update_personal_goal(user_id, goal):
    sql = "UPDATE personal_details SET personal_goal=:personal_goal WHERE user_id=:user_id"
    db.session.execute(sql, {"personal_goal":goal, "user_id":user_id})
    db.session.commit()
    return True

def has_profile(user_id):
    sql = "SELECT id FROM personal_details WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    if result.fetchone() == None:
        return False
    else:
        return True

def add_personal_details(user_id, gender_id, age, height, weight, activity):
    if has_profile(user_id):
        update_personal_details(user_id, gender_id, age, height, weight, activity)
    else:
        sql = "INSERT INTO personal_details (user_id, gender_id, age, height, weight, activity) " \
            "VALUES (:user_id, :gender_id, :age, :height, :weight, :activity)"
        db.session.execute(sql, {"user_id":user_id, "gender_id":gender_id, "age":age, \
            "height":height, "weight":weight, "activity":activity})
        db.session.commit()
    calorie_goal = count_calorie_goal(gender_id, age, height, weight, activity)
    fooddiaries.update_todays_goal(user_id, calorie_goal)
    return True

def update_personal_details(user_id, gender_id, age, height, weight, activity):
    sql = "UPDATE personal_details SET gender_id=:gender_id, age=:age, height=:height, weight=:weight, " \
        "activity=:activity WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id, "gender_id":gender_id, "age":age, \
        "height":height, "weight":weight, "activity":activity})
    db.session.commit()
    return True


def count_calorie_goal(gender_id, age, height, weight, activity):
    if gender_id == 1:
        calorie_goal = round(float(activity) * (447.593 + (9.247 * float(weight)) + \
            (3.098 * float(height)) - (4.33 * float(age))))
    else:
        calorie_goal = round(float(activity) * (88.362 + (13.397 * float(weight)) + \
            (4.799 * float(height)) - (5.677 * float(age))))
    return calorie_goal

def count_calorie_goal_by_id(user_id):
    details = get_personal_details(user_id)
    if details == None:
        return None
    else:
        gender_id = details[0]
        age = details[1]
        height = details[2]
        weight = details[3]
        activity = details[4]
        calorie_goal = count_calorie_goal(gender_id, age, height, weight, activity)
        return calorie_goal

def get_gender(gender_id):
    sql = "SELECT gender FROM gender WHERE id=:gender_id"
    result = db.session.execute(sql, {"gender_id":gender_id})
    gender = result.fetchone()[0]
    return gender

