from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CountryFilters
from .persistence import get_countries, get_country_by_code
from .serializers import CountrySerializer


class CountryList(ListCreateAPIView):
    serializer_class = CountrySerializer
    queryset = get_countries()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountryFilters

    @extend_schema(responses=CountrySerializer,
                   parameters=[OpenApiParameter(name="minPopulation", type=int),
                               OpenApiParameter(name="maxPopulation", type=int),
                               OpenApiParameter(name="incomeLevel", type=str, enum=["HIC", "UMC", "LMC", "LIC"])])
    def get(self, request, *args, **kwargs):
        return super().get(request)


class CountryDetailView(APIView):
    def get(self, request, code):
        """
        Retrieves the Country with given code
        """
        country_instance = get_country_by_code(code)
        serializer = CountrySerializer(country_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
