import sqlite3
import requests

#MEAL_TYPES = ["breakfast","main course","vegetarian","vegan","pescatarian"]
MEAL_TYPES = ["main course"]

kei_key = "402cf8980ef54e318fba1bd772fd3dde"
leah_key = "41b38bcafc974c06937752cda574f500"
alvin_key = "6d081c60d7aa4cd8b2ad2e3c810ef703"
alvin_key2 = "5e1b1107f24d4d1cbc92bb5e681813ab"
API_KEY = alvin_key2.strip() #use ur own when you can
API_URL = "https://api.spoonacular.com/recipes/complexSearch"




def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        summary TEXT,
        instructions TEXT,
        ingredients TEXT,
        calories INT,
        protein INT,
        fat INT,
        fiber INT,
        image_url TEXT,
        servings INT,
        ready_in_minutes INT,
        source_url TEXT,
        diets TEXT,
        cuisines TEXT,
        very_healthy BOOL,
        like_count INT,
        spoonacular_score REAL,
        meal_type TEXT
                
    )
    """)
    conn.commit()
    

def add_to_table(meal_type,conn):
    params = {
        "apiKey": API_KEY,
        "query": meal_type,
        "number": 100, #limits results we get to 5
        "addRecipeInformation" : True, #gives us the recipe descriptions
        "addRecipeNutrition" : True,
        "offset": 650,
        "instructionsRequired": True,
  
    }
    response = requests.get(API_URL,params)
    if response.status_code != 200:#if the request didnt fail
        print(f"API failed for {meal_type}: {response.status_code}")
        return
    data = response.json()    
    recipes = data.get("results",[]) #give me the results array if it exists, else give me an empty list

    if not recipes:
        return
    
    cursor = conn.cursor()
    inserted = 0


    for r in recipes:
        #nutrients are its own subsection from the recipe info
        nutrients_list = r.get("nutrition", {}).get("nutrients", [])
        nut_dict = {n.get("name"): n.get("amount") for n in nutrients_list}
        # the question marks are used so i can insert variables
        #or ignore is to account for duplicate recipes
        #ingredients
        ingredients_set = set()  # avoid duplicates
        for instr in r.get("analyzedInstructions", []):
            for step in instr.get("steps", []):
                for ing in step.get("ingredients", []):
                    name = ing.get("name")
                    if name:
                        ingredients_set.add(name.strip())

        ingredients_text = ", ".join(sorted(ingredients_set)) if ingredients_set else None
        #instructions
        instructions_parts = []
        for section in r.get("analyzedInstructions", []):
            for step in section.get("steps", []):
                step_text = step.get("step", "").strip()
                if step_text:
                    instructions_parts.append(step_text)

        instructions_text = "\n".join(instructions_parts) if instructions_parts else None
        cursor.execute("""
            INSERT OR IGNORE INTO recipes ( 
                id,
                title,
                summary,
                instructions,
                ingredients,
                calories,
                protein,
                fat,
                fiber,
                image_url,
                servings,
                ready_in_minutes,
                source_url,
                diets,
                cuisines,
                very_healthy,
                like_count,
                spoonacular_score,
                meal_type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            r.get("id"),
            r.get("title"),
            r.get("summary", ""),
            instructions_text,
            ingredients_text,

            nut_dict.get("Calories"),
            nut_dict.get("Protein"),
            nut_dict.get("Fat"),
            nut_dict.get("Fiber"),

            r.get("image"),
            r.get("servings"),
            r.get("readyInMinutes"),
            r.get("sourceUrl"),
            ",".join(r.get("diets", [])) or None,
            ",".join(r.get("cuisines", [])) or None,
            r.get("veryHealthy", False),
            r.get("aggregateLikes"),
            r.get("spoonacularScore"),
            meal_type
        ))
        if cursor.rowcount > 0:
            inserted += 1
    
    conn.commit()
    print(f"{meal_type}: inserted {inserted} new recipes (total tried: {len(recipes)})")



def main():
    conn = sqlite3.connect("recipes.db")
    create_table(conn)
    for meal in MEAL_TYPES:
        add_to_table(meal,conn)
    conn.close()
    

if __name__ == "__main__":
    main()