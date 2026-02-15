import sqlite3

def query_simple(conn, ingredients_list): #grabs all recipes that include ALL the ingredients
    cursor = conn.cursor()

    query = "SELECT id,title,like_count FROM recipes WHERE "
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
    conn = sqlite3.connect("recipes.db")
    user_query = input("Enter your ingredients seperated by spaces:\n")
    ingredients_list = user_query.split()
    print(query_simple(conn,ingredients_list))