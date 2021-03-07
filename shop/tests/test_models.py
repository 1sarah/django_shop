from django.test import TestCase
from datetime import datetime

from ..models import Customer, Order


class CustomerTestCase(TestCase):
    def test_customer(self):
        self.assertEquals(
            Customer.objects.count(),
            0
        )
        Customer.objects.create(
            name='cust1', code=111
        )
        Customer.objects.create(
            name='cust2', code=222
        )
        self.assertEquals(
            Customer.objects.count(),
            2
        )


class OrderTestCase(TestCase):
    def test_order(self):
        self.assertEquals(
            Order.objects.count(),
            0
        )
        cust1 = Customer.objects.create(
             name='cust1', code=111
        )
        Order.objects.create(item='watch', amount=100, time=datetime(2021, 3, 1,23, 55, 59), customer=cust1)
        self.assertEquals(
            Order.objects.count(),
            1
        )
