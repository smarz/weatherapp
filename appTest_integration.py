import unittest
from app import app, db, Weather, get_temperature

class TestDataIntegration(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    def test_data_collection_and_display_avg_temp(self):
        city = "Boulder"
        temperature, date_time, description, icon, country, lat, lon = get_temperature(city)

        self.assertIsNotNone(temperature)
        self.assertIsNotNone(date_time)

        response = self.app.get('/average_temp', follow_redirects=True)  # Set follow_redirects to True

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
