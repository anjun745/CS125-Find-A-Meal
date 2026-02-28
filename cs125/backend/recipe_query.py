import sqlite3
MEAL_TYPE_MAP = {
    "breakfast": [
        "breakfast"
    ],

    "lunch": [
        "salad",
        "soup",
        "side dish",
        "bread",
        "appetizer"
    ],

    "dinner": [
        "main course",
        "soup",
        "side dish"
    ]
}

def query_simple(conn, ingredients_list, allergy=None, meal_type=None): #grabs all recipes that include ALL the ingredients
    cursor = conn.cursor()

    query = "SELECT id, title, image_url, calories, ready_in_minutes, source_url FROM recipes "
    conditions = []
    params = []
    for ingredient in ingredients_list:
        conditions.append("LOWER(ingredients) LIKE LOWER(?)")
        params.append(f"%{ingredient}%")

    # exclude allergies
    if allergy:
        allergies = allergy if isinstance(allergy, (list, tuple, set)) else [allergy]
        for a in allergies:
            conditions.append("LOWER(ingredients) NOT LIKE LOWER(?)")
            params.append(f"%{a}%")

    # filter meal type
    if meal_type:
        meal_types = MEAL_TYPE_MAP.get(meal_type.lower(), [])
        if meal_types:
            placeholders = ",".join(["?"] * len(meal_types))
            conditions.append(f"LOWER(meal_type) IN ({placeholders})")
            params.extend([m.lower() for m in meal_types])
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results

def query_with_extras(conn, ingredients_list,
    min_calories=None,
    max_calories=None,
    min_protein=None,
    max_protein=None,
    min_fiber=None,
    max_fiber=None,
    min_fat=None,
    max_fat=None, allergy=None, meal_type=None): #grabs all recipes that include ALL the ingredients
    cursor = conn.cursor()
    print("MIN AND MAX PROTEIN:", min_protein, max_protein)
    print("MIN AND MAX CALORIES:", min_calories, max_calories)
    query = "SELECT id, ingredients, title, image_url, calories, ready_in_minutes, source_url, meal_type FROM recipes WHERE "
    print("ALLERGY:", allergy)
    conditions = []
    params = []
    for ingredient in ingredients_list:
        conditions.append("(LOWER(ingredients) LIKE LOWER(?) OR LOWER(title) LIKE LOWER(?))")
        params.append(f"%{ingredient}%")
        params.append(f"%{ingredient}%")

    if min_calories is not None:
        conditions.append("calories >= ?")
        params.append(min_calories)

    if max_calories is not None:
        conditions.append("calories <= ?")
        params.append(max_calories)

    if min_protein is not None:
        conditions.append("protein >= ?")
        params.append(min_protein)

    if max_protein is not None:
        conditions.append("protein <= ?")
        params.append(max_protein)

    if min_fiber is not None:
        conditions.append("fiber >= ?")
        params.append(min_fiber)

    if max_fiber is not None:
        conditions.append("fiber <= ?")
        params.append(max_fiber)

    if min_fat is not None:
        conditions.append("fat >= ?")
        params.append(min_fat)

    if max_fat is not None:
        conditions.append("fat <= ?")
        params.append(max_fat)
    
    if allergy:
        allergies = allergy if isinstance(allergy, (list, tuple, set)) else [allergy]
        for a in allergies:
            conditions.append("LOWER(ingredients) NOT LIKE LOWER(?)")
            params.append(f"%{a}%")
    if meal_type:
        meal_types = MEAL_TYPE_MAP.get(meal_type.lower(), [])

        if meal_types:
            placeholders = ",".join(["?"] * len(meal_types))
            conditions.append(f"LOWER(meal_type) IN ({placeholders})")
            params.extend([m.lower() for m in meal_types])
    query += " AND ".join(conditions)

    title_score_parts = []
    title_params = []

    for ingredient in ingredients_list:
        title_score_parts.append(
            "CASE WHEN LOWER(title) LIKE LOWER(?) THEN 100 ELSE 0 END"
        )
        title_params.append(f"%{ingredient}%")

    score_expression = "like_count + " + " + ".join(title_score_parts)

    query += f" ORDER BY ({score_expression}) DESC"

    params.extend(title_params) #we need this cause otherwise we still have an extra unfilled ?
    cursor.execute(query, params)
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results

def query_simple_or(conn, ingredients_list, allergy=None): #grabs all recipes that include ANY the ingredients
    cursor = conn.cursor()

    query = "SELECT id, title, image_url, calories, ready_in_minutes, source_url, meal_type FROM recipes WHERE "
    conditions = []
    params = []

    for ingredient in ingredients_list:
        conditions.append("ingredients LIKE ?")
        params.append(f"%{ingredient}%")

    query += " OR ".join(conditions)
    if allergy:
        allergies = allergy if isinstance(allergy, (list, tuple, set)) else [allergy]
        for a in allergies:
            query += " AND LOWER(ingredients) NOT LIKE LOWER(?)"
            params.append(f"%{a}%")
            
    query += " ORDER BY like_count DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results

def recommendations(conn, allergy=None, meal_type=None, min_calories=None, max_calories=None, limit=20):
    sql = """
    SELECT id, title, image_url, calories, ready_in_minutes, source_url, meal_type
    FROM recipes
    WHERE 1=1
    """
    params = []

    if meal_type:
        mapped = MEAL_TYPE_MAP.get(meal_type.lower(), [meal_type.lower()])

        like_clauses = []
        for mt in mapped:
            like_clauses.append("LOWER(meal_type) LIKE ?")
            params.append(f"%{mt.lower()}%")

        sql += " AND (" + " OR ".join(like_clauses) + ")"

    if min_calories is not None:
        sql += " AND calories >= ?"
        params.append(min_calories)

    if max_calories is not None:
        sql += " AND calories <= ?"
        params.append(max_calories)

    if allergy:
        allergies = allergy if isinstance(allergy, (list, tuple, set)) else [allergy]
        for a in allergies:
            sql += " AND LOWER(ingredients) NOT LIKE LOWER(?)"
            params.append(f"%{a}%")

    sql += " ORDER BY RANDOM()"
    sql += " LIMIT ?"
    params.append(limit)

    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()

    columns = [col[0] for col in cur.description]
    return [dict(zip(columns, row)) for row in rows]