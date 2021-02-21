from db import db


def get_foodstuffs():
    sql = "SELECT * FROM foodstuffs"
    result = db.session.execute(sql)
    return result.fetchall()

def get_foodstuff_by_name(food_name):
    sql = "SELECT * FROM foodstuffs WHERE name ILIKE :name"
    result = db.session.execute(sql, {"name":'%%'+food_name+'%%'})
    return result.fetchall()

def dictionary(foodstuff):
    dictionary = {
	    "id": foodstuff[0],
	    "name": foodstuff[1],
	    "calories": foodstuff[2],
	    "fat": foodstuff[3],
	    "carbs": foodstuff[4],
	    "protein": foodstuff[5],
	    "fiber": foodstuff[6]
        }
    return dictionary

def foodstuffs_to_dictionary(foodstuffs):
    foodstuffs = []
    for foodstuff in foodstuffs:
        foodstuffs.append(dictionary(foodstuff))
    return foodstuffs

