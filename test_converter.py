from main import app
from country import countries_info
import unittest

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_strict_format(self):
        # Test valid strict format
        response = self.app.post('/currency_converter', data={
            'country1': 'India (IN) : INR - Indian Rupee',
            'country2': 'United States (US) : USD - US Dollar',
            'rate1': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result', response.data)

    def test_partial_match(self):
        # Test just country name
        response = self.app.post('/currency_converter', data={
            'country1': 'India',
            'country2': 'United States',
            'rate1': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Result', response.data)

    def test_invalid_input(self):
        # Test invalid country
        response = self.app.post('/currency_converter', data={
            'country1': 'Mars',
            'country2': 'United States',
            'rate1': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid format for Country 1', response.data)

if __name__ == '__main__':
    unittest.main()
