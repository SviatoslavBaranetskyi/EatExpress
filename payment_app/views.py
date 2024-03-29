from django.http import HttpResponseRedirect
from cloudipsp import Api, Checkout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from delivery_app.models import Order


class PaymentView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        api = Api(merchant_id=1396424, secret_key='test')
        checkout = Checkout(api=api)
        data = {
            "currency": "USD",
            "amount": int(float(order.total_price) * 100)
        }
        url = checkout.url(data).get('checkout_url')
        print(url)
        return HttpResponseRedirect(url)
