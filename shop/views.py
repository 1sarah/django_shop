from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer


class CustomerListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of customers or create new
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete customer
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class OrderListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of orders or create new
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete order
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class CreateOrderAPIView(APIView):
    serializer_class = OrderSerializer

    def post(self, request, customer_pk):
        # customer_pk = request.data.get("customer_pk")
        request.data['customer'] = customer_pk
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            # data to return
            customer = order.customer
            serializer.data['customer'] = customer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)