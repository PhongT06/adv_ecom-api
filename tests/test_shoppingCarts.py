import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestShoppingCartEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.shoppingCartService.get_shopping_cart')
    def test_get_cart(self, mock_get):
        customer_id = fake.random_int()
        product_id = fake.random_int()
        quantity = fake.random_int()
        total = fake.pyfloat()
        mock_cart = MagicMock()
        mock_cart.id = 1
        mock_cart.customer_id = customer_id
        mock_cart.product_id = product_id
        mock_cart.quantity = quantity
        mock_cart.total = total
        mock_get.return_value = mock_cart

        payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "total": total
            }
        
        response = self.app.get(f'/shopping-cart/{mock_cart.id}', json=payload)
        self.assertEqual(response.status_code, 404)