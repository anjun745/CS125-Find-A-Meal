import sqlite3

def query_simple(conn, ingredients_list): #grabs all recipes that include ALL the ingredients
    cursor = conn.cursor()

    query = "SELECT id,like_count FROM recipes WHERE "
    conditions = []
    params = []

    for ingredient in ingredients_list:
        conditions.append("ingredients LIKE ?")
        params.append(f"%{ingredient}%")

    query += " AND ".join(conditions)
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    #return [row[0] for row in results] #gets us the id without parenthesis or comma
    return results 

def query_simple_or(conn, ingredients_list): #grabs all recipes that include ANY the ingredients
    cursor = conn.cursor()

    query = "SELECT id,like_count FROM recipes WHERE "
    conditions = []
    params = []

    for ingredient in ingredients_list:
        conditions.append("ingredients LIKE ?")
        params.append(f"%{ingredient}%")

    query += " OR ".join(conditions)
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    return [row[0] for row in results] #gets us the id without parenthesis or comma

if __name__ == "__main__":
    ingredients_list = ["chicken", "garlic", "rice"]
    conn = sqlite3.connect("recipes.db")
    print(query_simple(conn,ingredients_list))