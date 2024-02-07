import unittest

recipes= {
    'name': 'Carrot'
}

class TestRecipe(unittest.TestCase):
    def test_parse_carrot(self):
        self.assertIsInstance(recipes[0], dict, "The `parse_recipe` method should return a `dict` object")
