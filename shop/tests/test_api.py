from datetime import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from ..models import Customer, Order


class CustomerListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-customer-list')

    def test_create_customer(self):
        self.assertEquals(
            Customer.objects.count(),
            0
        )
        data = {
            'name': 'cust1',
            'code': 111
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Customer.objects.count(),
            1
        )
        customer = Customer.objects.first()
        self.assertEquals(
            customer.name,
            data['name']
        )
        self.assertEquals(
            customer.code,
            data['code']
        )

    def test_get_customer_list(self):
        order = Order(item='watch', amount=100, time=datetime(2021, 3, 1,23, 55, 59))
        order.save()

        cust = Customer(
            name='cust1', code=111,
        )
        cust.save()
        cust.orders.add(order)

        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['name'],
            cust.name
        )
        self.assertEquals(
            data['code'],
            cust.code
        )

        self.assertEquals(
            data['orders'][0]['item'],
            order.item
        )

        self.assertEquals(
            data['orders'][0]['amount'],
            order.amount
        )
        self.assertIsNotNone(
            data['orders'][0]['time'],
        )


class CustomerDetailsAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.customer = Customer(
            name='cust1', code=111,
        )
        self.customer.save()
        self.url = reverse('api-customer-details', kwargs={'pk': self.customer.pk})

    def test_get_customer_details(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['id'],
            self.customer.pk
        )
        self.assertEquals(
            data['name'],
            self.customer.name
        )
        self.assertEquals(
            data['code'],
            self.customer.code
        )    

    def test_update_customer(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['name'] = 'new_name'
        data['code'] = 777
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.customer.refresh_from_db()
        self.assertEquals(
            self.customer.name,
            data['name']
        )
        self.assertEquals(
            self.customer.code,
            data['code']
        )

    def test_delete_customer(self):
        self.assertEquals(
            Customer.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Customer.objects.count(),
            0
        )

class OrderListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-order-list')
        self.customer = Customer.objects.create(
            name='cust1', code=111
        )

    def test_create_order(self):
        self.assertEquals(
            Order.objects.count(),
            0
        )
        data = {
            'item': 'watch',
            'amount': 200,
            'time': datetime(2021, 1, 10),
            'customer': self.customer.pk
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Order.objects.count(),
            1
        )
        order = Order.objects.first()
        self.assertEquals(
            order.item,
            data['item']
        )
        self.assertEquals(
            order.amount,
            data['amount']
        )

        self.assertEquals(
            data['customer'],
            order.customer.pk
        )

    def test_get_order_list(self):
        cust = Customer(
            name='cust1', code=111,
        )
        cust.save()
        order = Order(item='watch', amount=100, time=datetime(2021, 3, 1,23, 55, 59), customer=cust)
        order.save()
        
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['item'],
            order.item
        )
        self.assertEquals(
            data['amount'],
            order.amount
        )


class OrderDetailsAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.customer = Customer(
            name='cust1', code=111,
        )
        self.customer.save()
        self.order = Order(item='watch', amount=100, time=datetime(2021, 3, 1,23, 55, 59), customer=self.customer)
        self.order.save()
        self.url = reverse('api-order-details', kwargs={ 'pk': self.order.pk})

    def test_get_order_details(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['id'],
            self.order.pk
        )
        self.assertEquals(
            data['item'],
            self.order.item
        )
        self.assertEquals(
            data['amount'],
            self.order.amount
        )

    def test_update_order(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['amount'] = 999
        data['item'] = 'shirt'
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.order.refresh_from_db()
        self.assertEquals(
            self.order.item,
            data['item']
        )
        self.assertEquals(
            self.order.amount,
            data['amount']
        )

    def test_delete_order(self):
        self.assertEquals(
            Order.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Order.objects.count(),
            0
        )
