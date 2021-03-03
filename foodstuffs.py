from db import db



def get_foodstuff_by_name(food_name, user_id):
    sql = "SELECT * FROM foodstuffs WHERE name ILIKE :name AND (added_by=:user_id OR visible=true)"
    result = db.session.execute(sql, {"name":'%%'+food_name+'%%', "user_id":user_id})
    return result.fetchall()

def add_foodstuff(name, kcal, fat, carbs, pro, fiber, user_id):
    sql = "INSERT INTO foodstuffs (name, calories, fat, carbs, protein, fiber, added_by, visible) " \
        "VALUES (:name, :calories, :fat, :carbs, :protein, :fiber, :added_by, false)"
    db.session.execute(sql, {"name":name, "calories":kcal, "fat":fat, "carbs":carbs, "protein":pro, \
        "fiber":fiber, "added_by":user_id})
    db.session.commit()
    return True


