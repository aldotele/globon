from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .persistence import get_countries, get_country_by_code
from .serializers import CountrySerializer


class CountryListView(APIView):
    def get(self, request):
        queryset = get_countries().order_by('name')
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)


class CountryDetailView(APIView):
    def get(self, request, code):
        """
        Retrieves the Country with given code
        """
        country_instance = get_country_by_code(code)
        serializer = CountrySerializer(country_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
