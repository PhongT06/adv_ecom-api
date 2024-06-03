import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker
from auth import token_auth

fake = Faker()

class TestProductsEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.faker = Faker()

    def create_test_product(self):
        mock_product = MagicMock()
        mock_product.id = fake.uuid4()
        mock_product.name = fake.name()
        return mock_product

    @patch('services.productService.get_product')
    def test_get_product(self, mock_get):
        mock_product = self.create_test_product()
        mock_get.return_value = mock_product

        response = self.app.get(f'/products/{mock_product.id}')
        self.assertEqual(response.status_code, 404)