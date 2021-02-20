from db import db


def add_to_diary(user_id, foodstuff_id, meal_id, amount):
    sql_diary = "INSERT INTO food_diaries (user_id) VALUES (:user_id) RETURNING id"
    # allaoleva palauttaa yllä lisätyn rivin avaimen (= diary_id)
    diary_id = db.session.execute(sql_diary, {"user_id":user_id})
    sql_portions = "INSERT INTO portions (diary_id, foodstuff_id, meal_id, amount)" \
        "VALUES (:diary_id, :foodstuff_id, :meal_id, :amount)"
    db.session.execute(sql_portions, {"diary_id":diary_id, "foodstuff_id":foodstuff_id, "meal_id":meal_id, "amount":amount})

def get_todays_diary(user_id):
    sql = "SELECT * FROM food_diaries" \
        "INNER JOIN portions ON (food_diaries.id = portions.diary_id)" \
        "INNER JOIN foodstuffs ON (portions.foodstuff_id = foodstuffs.id)" \
        "INNER JOIN meals ON (meals.id = portions.meal_id)" \
        "WHERE user_id=:user_id AND date = current_date"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()