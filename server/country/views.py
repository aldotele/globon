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

    def post(self, request):
        filters = self.request.data
        queryset = get_countries()
        max_population = filters.get("maxPopulation")
        if max_population:
            queryset = queryset.filter(population__lte=max_population)
        min_population = filters.get("minPopulation")
        if min_population:
            queryset = queryset.filter(population__gte=min_population)

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
