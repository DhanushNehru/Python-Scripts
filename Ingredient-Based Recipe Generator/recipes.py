import random

# Expanded recipe data
recipes = {
    "Pasta": ["pasta", "tomato sauce", "cheese", "olive oil", "garlic"],
    "Omelette": ["eggs", "milk", "salt", "pepper", "cheese"],
    "Salad": ["lettuce", "tomato", "cucumber", "olive oil", "vinegar"],
    "Grilled Cheese": ["bread", "butter", "cheese"],
    "Smoothie": ["banana", "milk", "honey", "berries"],
    "Tacos": ["tortilla", "ground beef", "cheese", "lettuce", "sour cream"],
    "Pizza": ["pizza dough", "tomato sauce", "cheese", "pepperoni"],
    "Chicken Stir Fry": ["chicken breast", "bell pepper", "soy sauce", "rice", "garlic"],
    "Guacamole": ["avocado", "lime", "salt", "tomato", "onion"],
    "Pancakes": ["flour", "milk", "egg", "sugar", "baking powder"],
    "French Toast": ["bread", "egg", "milk", "cinnamon", "syrup"],
    "Baked Salmon": ["salmon", "lemon", "garlic", "olive oil", "salt"],
    "Stuffed Peppers": ["bell pepper", "rice", "ground beef", "cheese", "tomato sauce"],
    "Fried Rice": ["rice", "egg", "soy sauce", "peas", "carrot"],
    "Tomato Soup": ["tomato", "garlic", "onion", "basil", "cream"],
    "Mac and Cheese": ["macaroni", "cheese", "milk", "butter", "flour"],
    "Garlic Bread": ["bread", "garlic", "butter", "parsley", "cheese"],
    "Mashed Potatoes": ["potato", "butter", "milk", "salt", "pepper"],
    "Chocolate Cake": ["flour", "cocoa powder", "sugar", "eggs", "butter"],
    "Lemonade": ["lemon", "water", "sugar"],
    "Fruit Salad": ["apple", "banana", "berries", "orange", "grapes"],
    "Chicken Soup": ["chicken", "carrot", "celery", "onion", "broth"],
    "Bruschetta": ["bread", "tomato", "basil", "olive oil", "garlic"],
    "Beef Stew": ["beef", "potato", "carrot", "celery", "broth"],
    "Shrimp Scampi": ["shrimp", "garlic", "butter", "lemon", "pasta"]
}

# Function to suggest recipes based on starting letter
def suggest_recipes_by_letter(start_letter):
    suggestions = [recipe for recipe in recipes if recipe.lower().startswith(start_letter.lower())]
    return suggestions

# Get the starting letter input from the user
start_letter = input("Enter the starting letter for recipe suggestions: ").strip()

# Get recipe suggestions based on the starting letter
suggested_recipes = suggest_recipes_by_letter(start_letter)

# Output results
if suggested_recipes:
    print(f"Recipes that start with '{start_letter}':")
    for recipe in suggested_recipes:
        print(f"- {recipe}")
else:
    print(f"No recipes found starting with '{start_letter}'.")
