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

add_meal(cursor, "Quinoa Power Bowl",
         ["quinoa", "spinach", "tomato", "feta", "olive oil"],
         "Cook and cool quinoa. Toss with chopped spinach, tomato, and feta. Drizzle with olive oil, honey, and balsamic vinegar.")
         
add_meal(cursor, "Avocado Toast",
         ["whole grain bread", "avocado", "lemond juice", "sea salt", "black pepper"],
         "Toast bread. Mash avocado with lemon juice, a dash of salt and pepper. Then spread on toast." )

add_meal(cursor, "Greek Yogurt Parfait",
    ["plain Greek yogurt", "honey", "granola", "strawberries", "blueberries"],
    "Layer yogurt, drizzle honey, then granola and mixed berries. Serve immediately."
)

add_meal(cursor, "Buddha Bowl",
    ["brown rice", "roasted chickpeas", "steamed broccoli", "carrot ribbons", "hummus"],
    "Assemble rice, veggies, chickpeas and a dollop of hummus. Drizzle with lemon-tahini."
)

add_meal(cursor, "Spinach & Feta Egg Muffins",
    ["eggs", "spinach", "feta cheese", "salt", "pepper"],
    "Whisk eggs with chopped spinach and feta. Pour into muffin tin and bake at 350°F for 18–20 min."
)

add_meal(cursor, "Overnight Oats",
    ["old-fashioned oats", "almond milk", "chia seeds", "maple syrup", "banana slices"],
    "Combine all in jar, stir, refrigerate overnight. Top with banana before eating."
)


add_meal(cursor, "Honey Mustard Chicken Skewers",
    ["chicken breast", "honey", "Dijon mustard", "olive oil", "garlic", "salt", "pepper"],
    "Cut chicken into 1-inch cubes. Whisk honey, mustard, oil, minced garlic, salt & pepper. 3. Toss chicken in marinade and refrigerate 30 min. 4. Thread onto skewers and grill 4–5 min per side until cooked through."
)

add_meal(cursor, "One-Pan Lemon Garlic Chicken",
    ["chicken thighs", "lemon", "garlic", "olive oil", "rosemary", "salt", "pepper"],
    "Preheat oven to 400 °F. In a baking dish, place chicken thighs skin-side up. Drizzle olive oil, juice of half a lemon, minced garlic, chopped rosemary, salt & pepper over chicken. Roast 25–30 min until golden and juices run clear."
)

add_meal(cursor, "Chicken & Vegetable Stir-Fry",
    ["chicken breast", "bell pepper", "broccoli", "carrot", "soy sauce", "sesame oil", "garlic", "ginger"],
    "Slice chicken thinly and veggies into bite-size pieces. Heat oil in a wok; sauté garlic & ginger 30 sec. Add chicken and cook until no longer pink. Toss in vegetables, splash soy sauce, stir-fry 4–5 min until crisp-tender."
)

add_meal(cursor, "Slow-Cooker Shredded Chicken Tacos",
    ["chicken breasts", "tomato sauce", "chicken broth", "chili powder", "cumin", "onion powder", "tortillas"],
    "Place chicken in slow cooker. Pour tomato sauce, broth, and spices over top. Cook on low 6–7 hr (or high 3 hr). Shred chicken with forks and serve in warm tortillas with your favorite toppings."
)

# Saved and close
conn.commit()
conn.close()
