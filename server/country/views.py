from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CountryFilters
from .persistence import get_all_countries
from .serializers import CountrySerializer


@extend_schema(responses=CountrySerializer,
               parameters=[OpenApiParameter(name="incomeLevel", type=str, enum=["HIC", "UMC", "LMC", "LIC"]),
                           OpenApiParameter(name="iso3", type=str,
                                            description="unique identifier (ITA for Italy, DEU for Germany, ...)"),
                           OpenApiParameter(name="iso2", type=str,
                                            description="unique identifier (IT for Italy, DE for Germany, ...)"),
                           OpenApiParameter(name="fields", type=str,
                                            description='specify the fields you want to include as "field1,field2, ..."')])
class CountryList(APIView):
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountryFilters

    def get(self, request):
        query = self.filter_queryset(get_all_countries())
        serializer = CountrySerializer(
            query, many=True, fields=[field.strip() for field in request.query_params.get('fields').split(",")]) \
            if "fields" in request.query_params \
            else CountrySerializer(query, many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """
        taken from the GenericAPIView. In this way we can use the simpler APIView
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
