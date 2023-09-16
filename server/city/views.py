from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CityFilters
from .persistence import get_all_cities
from .serializers import CitySerializer


@extend_schema(responses=CitySerializer,
               parameters=[OpenApiParameter(name="iso3", type=str, description="3 characters identifier of the country"),
                           OpenApiParameter(name="smId", type=int, description="unique identifier of the city"),
                           OpenApiParameter(name="capital", type=bool, description="true if country capital"),
                           OpenApiParameter(name="countyCapital", type=bool, description="true if local capital"),
                           OpenApiParameter(name="minPopulation", type=int),
                           OpenApiParameter(name="maxPopulation", type=int),
                           ])
class CityList(APIView):
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CityFilters

    def get(self, request, format=None):
        if not request.query_params:
            return Response("please apply at least one filter", status=403)
        query = self.filter_queryset(get_all_cities())
        serializer = CitySerializer(query, many=True)
        results = serializer.data
        # TODO implement pagination
        if len(results) > 300:
            return Response("too many items", status=403)

        return Response(results)

    def filter_queryset(self, queryset):
        """
        taken from the GenericAPIView. In this way we can use the simpler APIView
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
