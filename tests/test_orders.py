import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestOrderEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.orderService.find_by_id')
    def test_get_order(self, mock_get):
        customer_id = fake.random_int()
        product_id = fake.random_int()
        quantity = fake.random_int()
        total = fake.pyfloat()
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.product_id = product_id
        mock_order.quantity = quantity
        mock_order.total = total
        mock_get.return_value = mock_order

        payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "total": total
            }
        
        response = self.app.get(f'/orders/{mock_order.id}', json=payload)

        self.assertEqual(response.status_code, 401)
