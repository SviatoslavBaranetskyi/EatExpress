import requests
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from profile_app.models import Profile
from .serializers import RestaurantSerializer


class RestaurantView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        address = profile.address

        geolocator = Nominatim(user_agent="geolocation")
        location = geolocator.geocode(address)

        url = "https://api.foursquare.com/v3/places/search"

        params = {
            "categories": request.GET.get("categories", "13000"),
            "ll": request.GET.get("ll", f"{location.latitude},{location.longitude}"),
            "open_now": request.GET.get("open_now", "true"),
            "sort": request.GET.get("sort", "DISTANCE"),
            "radius": 10000,
            "limit": 50
        }

        headers = {
            "Accept": "application/json",
            "Authorization": "fsq3tu1K/U81EMqCkX+uTBRPtXDkPSgPdky++rPee1VUkVc="
        }

        response = requests.get(url, params=params, headers=headers)

        data = response.json().get("results", [])

        if not data:
            return Response({'error': 'There are no restaurants available for delivery in your city'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantSerializer(data, many=True)
        return Response(serializer.data)
