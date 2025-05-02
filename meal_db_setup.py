import sqlite3

# Connect to database
conn = sqlite3.connect("meals.db")
cursor = conn.cursor()

# Create 'meals' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Create 'ingredients' table with meal_id
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meals(id)
)
""")

# Create 'recipes' table with meal_id
cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER,
    instructions TEXT NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meals(id)
)
""")

# Function to add meal, ingredients, and instructions
def add_meal(cursor, meal_name, ingredients, instructions):
    cursor.execute("INSERT INTO meals (name) VALUES (?)", (meal_name,))
    meal_id = cursor.lastrowid

    cursor.executemany("INSERT INTO ingredients (meal_id, name) VALUES (?, ?)", 
                       [(meal_id, ing) for ing in ingredients])

    cursor.execute("INSERT INTO recipes (meal_id, instructions) VALUES (?, ?)", 
                   (meal_id, instructions))

# Add meals
add_meal(cursor, "Vegan Chickpea Salad",
         ["chickpeas", "olive oil", "lemon juice", "cucumber", "tomato"],
         "Mix chickpeas with diced cucumber and tomato. Drizzle with olive oil and lemon juice. Toss and serve chilled.")

add_meal(cursor, "Tofu Stir Fry",
         ["tofu", "soy sauce", "bell pepper", "broccoli", "ginger"],
         "Sauté tofu until golden. Add sliced veggies and grated ginger. Stir in soy sauce and cook until veggies are tender.")

add_meal(cursor, "Grilled Chicken Bowl",
         ["chicken", "rice", "corn", "broccoli", "tomato", "onion", "avocado"],
         "Grill chicken, steam broccoli. Serve over rice with corn, tomato, onion, and avocado slices.")

add_meal(cursor, "Lemon Garlic Salmon",
         ["salmon", "lemon", "garlic", "butter", "dijon mustard", "honey"],
         "Combine lemon juice, garlic, butter, mustard, and honey. Bake salmon with sauce at 375°F for 15–20 minutes.")

add_meal(cursor, "Lentil Soup",
         ["lentils", "curry powder", "cumin", "tomato", "vegetable broth", "collard greens"],
         "Simmer lentils with broth, tomato, and spices. Add collard greens and cook until tender.")

add_meal(cursor, "Ground Turkey Tacos",
         ["ground turkey", "tortillas", "tomato", "onion", "cilantro", "lemon", "avocado"],
         "Cook ground turkey with diced onion. Serve in tortillas with tomato, avocado, cilantro, and a squeeze of lemon.")

# Save and close
conn.commit()
conn.close()
