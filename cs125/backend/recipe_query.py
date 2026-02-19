import sqlite3

def query_simple(conn, ingredients_list): #grabs all recipes that include ALL the ingredients
    cursor = conn.cursor()

    query = "SELECT id, title, image_url, calories, ready_in_minutes, source_url FROM recipes WHERE "
    conditions = []
    params = []
    for ingredient in ingredients_list:
        conditions.append("ingredients LIKE ?")
        params.append(f"%{ingredient}%")

    query += " AND ".join(conditions)
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results


def query_simple_or(conn, ingredients_list): #grabs all recipes that include ANY the ingredients
    cursor = conn.cursor()

    query = "SELECT id, title, image_url, calories, ready_in_minutes, source_url FROM recipes WHERE "
    conditions = []
    params = []

    for ingredient in ingredients_list:
        conditions.append("ingredients LIKE ?")
        params.append(f"%{ingredient}%")

    query += " OR ".join(conditions)
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results


# if __name__ == "__main__":
#     conn = sqlite3.connect("recipes.db")
#     user_query = input("Enter your ingredients seperated by spaces:\n")
#     ingredients_list = user_query.split()
#     print(query_simple(conn,ingredients_list))