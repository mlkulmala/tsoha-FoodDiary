from db import db
import persons


def diary_exists(user_id):
    sql = "SELECT id FROM food_diaries WHERE user_id=:user_id AND date = current_date"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if result == None:
        return False
    return True


def add_to_diary(user_id, foodstuff_id, meal_id, amount):
    sql = "SELECT id FROM food_diaries WHERE user_id=:user_id AND date = current_date"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if result == None:
        diary_id = create_new_diary(user_id)
    else:
        diary_id = result[0]
    sql_portions = "INSERT INTO portions (diary_id, foodstuff_id, meal_id, amount)" \
        "VALUES (:diary_id, :foodstuff_id, :meal_id, :amount)"
    db.session.execute(sql_portions, {"diary_id":diary_id, "foodstuff_id":foodstuff_id, "meal_id":meal_id, "amount":amount})
    db.session.commit()
    return True


def create_new_diary(user_id):
    priority = persons.get_goal_priority(user_id)
    if priority:
        calorie_goal = persons.get_personal_goal
    else:
        if persons.has_profile(user_id):
            calorie_goal = persons.count_calorie_goal_by_id(user_id)
        else:
            calorie_goal = 2000
    sql = "INSERT INTO food_diaries (user_id, calorie_goal) VALUES (:user_id, :calorie_goal) RETURNING id"
    result = db.session.execute(sql, {"user_id":user_id, "calorie_goal":calorie_goal})
    db.session.commit()
    return result.fetchone()[0]


def update_todays_goal(user_id, calorie_goal):
    if diary_exists(user_id):
        sql = "UPDATE food_diaries SET calorie_goal=:calorie_goal WHERE user_id=:user_id AND date = current_date"
        db.session.execute(sql, {"user_id":user_id, "calorie_goal":calorie_goal})
        db.session.commit()
        return True
    else:
        sql_entry = "INSERT INTO food_diaries (user_id, calorie_goal) VALUES (:user_id, :calorie_goal)"
        db.session.execute(sql_entry, {"user_id":user_id, "calorie_goal":calorie_goal})
        db.session.commit()
        return True


def get_todays_goal(user_id):
    if diary_exists(user_id):
        sql = "SELECT calorie_goal FROM food_diaries WHERE user_id=:user_id AND date = current_date"
        result = db.session.execute(sql, {"user_id":user_id}).fetchone()
        return result[0]
    elif persons.get_goal_priority(user_id):
        calorie_goal = persons.get_personal_goal(user_id)
    elif persons.has_profile(user_id):
        calorie_goal = persons.count_calorie_goal_by_id(user_id)
    else:
        calorie_goal = 2000
    return calorie_goal



def get_calorie_goal_by_date(user_id, date):
    sql = "SELECT calorie_goal FROM food_diaries WHERE user_id=:user_id AND date=:date"
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    calorie_goal = result.fetchone()
    if calorie_goal == None:
        return None
    return calorie_goal[0]


def get_todays_diary(user_id):
    sql = "SELECT portions.id, meals.id, meals.name, foodstuffs.name, amount, calories, " \
        "fat, carbs, protein, fiber FROM food_diaries " \
        "INNER JOIN portions ON (food_diaries.id = portions.diary_id) " \
        "INNER JOIN foodstuffs ON (portions.foodstuff_id = foodstuffs.id) " \
        "INNER JOIN meals ON (meals.id = portions.meal_id) " \
        "WHERE user_id=:user_id AND date = current_date " \
        "ORDER BY meals.id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def get_diary_by_date(user_id, date):
    sql = "SELECT meals.id, meals.name, foodstuffs.name, amount, "\
        "calories, fat, carbs, protein, fiber FROM food_diaries " \
        "INNER JOIN portions ON (food_diaries.id = portions.diary_id) " \
        "INNER JOIN foodstuffs ON (portions.foodstuff_id = foodstuffs.id) " \
        "INNER JOIN meals ON (meals.id = portions.meal_id) " \
        "WHERE user_id=:user_id AND date=:date " \
        "ORDER BY date DESC, meals.id"
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    return result.fetchall()


def get_calories_and_nutrients(user_id, date):
    sql = "SELECT portions.amount, calories, fat, carbs, protein, fiber FROM foodstuffs " \
        "INNER JOIN portions ON (portions.foodstuff_id = foodstuffs.id) " \
        "INNER JOIN food_diaries ON (food_diaries.id = portions.diary_id) " \
        "WHERE user_id=:user_id AND date=:date"
    result = db.session.execute(sql, {"user_id":user_id, "date":date})
    rows = result.fetchall()
    if len(rows) == 0:
        return [0, 0, 0, 0, 0]
    else:
        # count total amount of each nutrient per each diary entry
        total_kcal, total_fat, total_carbs, total_protein, total_fiber = 0, 0, 0, 0, 0
        for row in rows:
            total_kcal += row[0] / 100 * row[1]
            total_fat += row[0] / 100 * float(row[2])
            total_carbs += row[0] / 100 * float(row[3])
            total_protein += row[0] / 100 * float(row[4])
            total_fiber += row[0] / 100 * float(row[5])
        # count the percentage of energy received from each nutrient
        kcal = round(total_kcal)
        fat = round(total_fat * 900 / total_kcal, 1)
        carbs = round(total_carbs * 400 / total_kcal, 1)
        pro = round(total_protein * 400 / total_kcal, 1)
        fiber = round(total_fiber)
        values = [kcal, fat, carbs, pro, fiber]
        return values


def delete_portion(id):
    sql = "DELETE FROM portions WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True


def get_portion(id):
    sql = "SELECT meals.name, foodstuffs.name, amount FROM portions " \
        "INNER JOIN foodstuffs ON foodstuffs.id = portions.foodstuff_id " \
        "INNER JOIN meals ON meals.id = portions.meal_id " \
        "WHERE portions.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()
