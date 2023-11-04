from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CountryFilters, CountryGeographyFilters, CountryEconomyFilters, CountrySocietyFilters
from .models import Country, CountryGeography, CountryEconomy, CountrySociety
from .serializers import CountrySerializer, CountryGeographySerializer, CountryEconomySerializer, \
    CountrySocietySerializer


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
        query = self.filter_queryset(Country.objects.all())
        serializer = CountrySerializer(
            query, many=True, fields=[field.lower().strip() for field in request.query_params.get('fields').split(",")]) \
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


@extend_schema(responses=CountryGeographySerializer,
               parameters=[OpenApiParameter(name="iso3", type=str,
                                            description="unique identifier (ITA for Italy, DEU for Germany, ...)"),
                           OpenApiParameter(name="fields", type=str,
                                            description='specify the fields you want to include as "field1,field2, ..."')])
class CountryGeographyList(APIView):
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountryGeographyFilters

    def get(self, request):
        query = self.filter_queryset(CountryGeography.objects.all())
        serializer = CountryGeographySerializer(
            query, many=True, fields=[field.lower().strip() for field in request.query_params.get('fields').split(",")]) \
            if "fields" in request.query_params \
            else CountryGeographySerializer(query, many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """
        taken from the GenericAPIView. In this way we can use the simpler APIView
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


@extend_schema(responses=CountryEconomySerializer,
               parameters=[OpenApiParameter(name="iso3", type=str,
                                            description="unique identifier (ITA for Italy, DEU for Germany, ...)"),
                           OpenApiParameter(name="fields", type=str,
                                            description='specify the fields you want to include as "field1,field2, ..."')])
class CountryEconomyList(APIView):
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountryEconomyFilters

    def get(self, request):
        query = self.filter_queryset(CountryEconomy.objects.all())
        serializer = CountryEconomySerializer(
            query, many=True, fields=[field.lower().strip() for field in request.query_params.get('fields').split(",")]) \
            if "fields" in request.query_params \
            else CountryEconomySerializer(query, many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """
        taken from the GenericAPIView. In this way we can use the simpler APIView
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


@extend_schema(responses=CountrySocietySerializer,
               parameters=[OpenApiParameter(name="iso3", type=str,
                                            description="unique identifier (ITA for Italy, DEU for Germany, ...)"),
                           OpenApiParameter(name="fields", type=str,
                                            description='specify the fields you want to include as "field1,field2, ..."')])
class CountrySocietyList(APIView):
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CountrySocietyFilters

    def get(self, request):
        query = self.filter_queryset(CountrySociety.objects.all())
        serializer = CountrySocietySerializer(
            query, many=True, fields=[field.lower().strip() for field in request.query_params.get('fields').split(",")]) \
            if "fields" in request.query_params \
            else CountrySocietySerializer(query, many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """
        taken from the GenericAPIView. In this way we can use the simpler APIView
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class CountryFieldList(APIView):
    def get(self, request):
        return Response(Country.get_field_names())


class CountryGeographyFieldList(APIView):
    def get(self, request):
        return Response(CountryGeography.get_field_names())


class CountryEconomyFieldList(APIView):
    def get(self, request):
        return Response(CountryEconomy.get_field_names())


class CountrySocietyFieldList(APIView):
    def get(self, request):
        return Response(CountrySociety.get_field_names())
