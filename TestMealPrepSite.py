class TestMealPrepSite(unittest.TestCase):

    def setUp(self):
        self.user = User()
        self.breakfast_meal = Meal("Oatmeal", "breakfast")
        self.lunch_meal = Meal("Salad", "lunch")
        self.dinner_meal = Meal("Pasta", "dinner")
        self.snack_meal = Meal("Fruit", "snacks")

        self.all_meals = [
            self.breakfast_meal,
            self.lunch_meal,
            self.dinner_meal,
            self.snack_meal
        ]

    def test_add_meals_to_day(self):
        self.user.add_meal_to_day("Monday", self.breakfast_meal)
        self.assertIn(self.breakfast_meal, self.user.days["Monday"].meals["breakfast"])

    def test_meals_added_to_correct_type(self):
        self.user.add_meal_to_day("Tuesday", self.lunch_meal)
        self.user.add_meal_to_day("Tuesday", self.dinner_meal)
        self.assertIn(self.lunch_meal, self.user.days["Tuesday"].meals["lunch"])
        self.assertIn(self.dinner_meal, self.user.days["Tuesday"].meals["dinner"])
        self.assertNotIn(self.lunch_meal, self.user.days["Tuesday"].meals["breakfast"])

    def test_filter_meals_by_type(self):
        filtered = self.user.filter_meals(self.all_meals, meal_type="snacks")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "Fruit")

    def test_like_and_read_meals(self):
        self.user.like_meal(self.dinner_meal)
        self.user.read_meal(self.dinner_meal)
        self.assertTrue(self.dinner_meal.liked)
        self.assertTrue(self.dinner_meal.read)

    def test_search_meal_by_name(self):
        results = self.user.search_meals("pasta", self.all_meals)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Pasta")

if __name__ == '__main__':
    unittest.main()
