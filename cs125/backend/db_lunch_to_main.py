import sqlite3

conn = sqlite3.connect("recipes.db")
cursor = conn.cursor()

cursor.execute("""
    UPDATE recipes
    SET meal_type = 'main course'
    WHERE meal_type = 'dinner'
""")

conn.commit()
print(f"{cursor.rowcount} rows updated.")
conn.close()
