from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id, username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = user[2]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def personal_details(user_id):
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

def get_gender(gender_id):
    sql = "SELECT gender FROM gender WHERE id=:gender_id"
    result = db.session.execute(sql, {"gender_id":gender_id})
    gender = result.fetchone()[0]
    return gender
