import requests
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from profile_app.models import Profile
from .serializers import RestaurantMenuSerializer


class RestaurantMenuView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url = "http://127.0.0.1:8000/api/v1/menu/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                serializer = RestaurantMenuSerializer(data=response.json(), many=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed to fetch restaurant data"}, status=response.status_code)
        except Exception as e:
            return Response({"message": f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
