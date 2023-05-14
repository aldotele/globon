from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CountryFilters
from .persistence import get_countries, get_all_languages
from .serializers import CountrySerializer


@extend_schema(responses=CountrySerializer,
               parameters=[OpenApiParameter(name="incomeLevel", type=str, enum=["HIC", "UMC", "LMC", "LIC"])])
class CountryList(ListCreateAPIView):
    http_method_names = ["get"]
    serializer_class = CountrySerializer
    queryset = get_countries()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountryFilters


class LanguageView(APIView):
    def get(self, request):
        return Response(get_all_languages(), status=status.HTTP_200_OK)

