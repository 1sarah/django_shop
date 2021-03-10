import rest_framework.decorators
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import update_last_login
from django.http import JsonResponse
from requests.models import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer, UserLoginSerializer, UserSerializer, SocialAuthSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class CustomerListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of customers or create new
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class CustomerDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete customer
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class OrderListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of orders or create new
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class OrderDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete order
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class CreateOrderAPIView(APIView):
    serializer_class = OrderSerializer

    def post(request, customer_pk):
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

    @rest_framework.decorators.api_view(['POST'])
    def social_login(request):
        serializer_class = SocialAuthSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        authenticated_user = request.user if not request.user.is_anonymous else None
        provider = serializer.data.get('provider')
        strategy = load_strategy(request)
        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return JsonResponse({"error": "Provider invalid or not supported"},
                                status=status.HTTP_404_NOT_FOUND)
        if isinstance(backend, BaseOAuth1):
            tokenn = {
                'oauth_token': serializer.data.get('access_token'),
                'oauth_token_secret': serializer.data.get('access_token_secret')
            }
        elif isinstance(backend, BaseOAuth2):
            tokenn = serializer.data.get('access_token')
        try:
            user = backend.do_auth(tokenn, user=authenticated_user)
        except BaseException as e:
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user.is_verified = True
            # user.token = functionto generate token

            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            user.tokenn = jwt_token
            print("+" * 10)
            print(jwt_token)
            user.save()
            update_last_login(None, user)
            serializer = UserSerializer(user)
            serializer.instance = user

            # import pdb;pdb.set_trace()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @rest_framework.decorators.api_view(['GET', 'POST'])
    def UserLoginView(request):
        permission_classes = (AllowAny,)
        serializer_class = UserLoginSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'tokenn': serializer.data['tokenn'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
