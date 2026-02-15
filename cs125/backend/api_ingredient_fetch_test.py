import requests

API_KEY = "5e1b1107f24d4d1cbc92bb5e681813ab"
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

params = {
    "apiKey": API_KEY,
    "query": "chicken",
    "number": 1,
    "addRecipeInformation": True,
    "instructionsRequired": True
}

response = requests.get(API_URL, params=params)

if response.status_code != 200:
    print("API failed:", response.status_code)
else:
    data = response.json()
    recipes = data.get("results", [])
    if not recipes:
        print("No recipes found")
    else:
        r = recipes[0]  # take the first recipe
        ingredients_list = []
        for instr in r.get("analyzedInstructions", []):
            for step in instr.get("steps", []):
                for ing in step.get("ingredients", []):
                    name = ing.get("name")
                    if name and name not in ingredients_list:
                        ingredients_list.append(name)
        print(ingredients_list)
        
        steps_list = []
        for instr in r.get("analyzedInstructions", []):
            for step in instr.get("steps", []):
                text = step.get("step")
                if text:
                    steps_list.append(text)
        print("\nInstruction Steps:")
        for i, s in enumerate(steps_list, 1):
            print(f"{i}. {s}")