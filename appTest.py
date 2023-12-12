import unittest
from unittest.mock import patch, MagicMock
from app import get_temperature, app

class TestGetTemp(unittest.TestCase):
    def test_valid_city(self):
        city = "Boulder"
        temperature, date_time, description, icon, country, lat, lon = get_temperature(city)

        # Ensure the returned temperature is not None
        self.assertIsNotNone(temperature)

        # Ensure other relevant information is available
        self.assertIsNotNone(date_time)
        self.assertIsNotNone(description)
        self.assertIsNotNone(icon)
        self.assertIsNotNone(country)
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

class MockTempTest(unittest.TestCase):

    @patch('app.requests.get')
    def test_valid_city(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 25.0},
            'dt': 1702261311,
            'weather': [{'description': 'Clear', 'icon': '01d'}],
            'sys': {'country': 'US'},
            'coord': {'lat': 40.0833, 'lon': -105.3505}
        }
        mock_get.return_value = mock_response

        temperature, date_time, description, icon, country, lat, lon = get_temperature("Boulder")
        self.assertEqual(temperature, 25.0)
        self.assertIsNotNone(description)
        self.assertIsNotNone(icon)
        self.assertIsNotNone(date_time)
        self.assertEqual(country, 'US')
        self.assertEqual(lat, 40.0833)
        self.assertEqual(lon, -105.3505)

    @patch('app.requests.get')
    def test_invalid_city(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'City not found'}
        mock_get.return_value = mock_response

        temperature, description, icon = get_temperature("FakeCity")
        self.assertIsNone(temperature)
        self.assertIsNone(description)
        self.assertIsNone(icon)

if __name__ == '__main__':
    unittest.main()
