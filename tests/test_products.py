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
        mock_product.id = self.faker.random_number(digits=3)
        mock_product.name = self.faker.word()
        mock_product.price = float(self.faker.random_number(digits=2))
        mock_product.stock_quantity = self.faker.random_number(digits=2)

        mock_product.__getitem__.side_effect = lambda key: getattr(mock_product, key)
        return mock_product

    def create_product_payload(self, mock_product):
        return {
            "name": mock_product.name,
            "price": mock_product.price,
            "stock_quantity": mock_product.stock_quantity
        }

    def test_get_products(self):
        response = self.app.get('/products/')
        self.assertEqual(response.status_code, 200)

    @patch('services.productService.get_product')
    def test_get_product(self, mock_get):
        mock_product = self.create_test_product()
        mock_get.return_value = mock_product

        response = self.app.get(f'/products/{mock_product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], mock_product.name)
