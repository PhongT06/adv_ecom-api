import unittest
from unittest.mock import patch
from faker import Faker
from app import create_app


fake = Faker()

class TestTokenEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.customerService.get_token')
    def test_success_authenticate(self, mock_token):
        mock_token.return_value = '12345'
        payload = {
            "username": fake.user_name(),
            'password': fake.password()
        }

        response = self.app.post('/token/', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['token'], '12345')

    @patch('services.customerService.get_token')
    def test_unauthorized_user(self, mock_token):
        mock_token.return_value = None
        payload = {
            "username": fake.user_name(),
            'password': fake.password()
        }

        response = self.app.post('/token/', json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['status'], 'error')
