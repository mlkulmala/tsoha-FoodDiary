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

