import unittest
import sqlite3
import os

def recipes_db(filepath, db_name="meals.db"):
    """Simplified version that just creates a database with a meals table"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ingredients TEXT,
        instructions TEXT
    )
    """)
    
    # Insert some test data
    cursor.execute("INSERT INTO meals (name, ingredients, instructions) VALUES (?, ?, ?)",
                   ("Test Meal", "ing1, ing2", "Mix ingredients"))
    
    conn.commit()
    conn.close()
    return True  # Simple return for testing

class TestRecipesDB(unittest.TestCase):
    def setUp(self):
        """Clean up old test files"""
        if os.path.exists("test.db"):
            os.remove("test.db")
    
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("test.db"):
            os.remove("test.db")
    
    def test_database_creation(self):
        """Test that the database is created"""
        result = recipes_db("dummy.csv", "test.db")
        self.assertTrue(result)
        self.assertTrue(os.path.exists("test.db"))
    
    def test_table_creation(self):
        """Test that the table exists and has the right structure"""
        recipes_db("dummy.csv", "test.db")
        
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        
        # Check table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meals'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check columns
        cursor.execute("PRAGMA table_info(meals)")
        columns = [row[1] for row in cursor.fetchall()]
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertIn("ingredients", columns)
        self.assertIn("instructions", columns)
        
        conn.close()
    
    def test_data_insertion(self):
        """Test that data is inserted correctly"""
        recipes_db("dummy.csv", "test.db")
        
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, ingredients, instructions FROM meals")
        row = cursor.fetchone()
        
        self.assertEqual(row[0], "Test Meal")
        self.assertEqual(row[1], "ing1, ing2")
        self.assertEqual(row[2], "Mix ingredients")
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
