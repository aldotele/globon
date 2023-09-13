from django.shortcuts import render
from django_filters import rest_framework
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CityFilters
from .persistence import get_cities
from .serializers import CitySerializer


# Create your views here.
@extend_schema(responses=CitySerializer,
               parameters=[OpenApiParameter(name="iso3", type=str)])
class CityList(ListCreateAPIView):
    http_method_names = ["get"]
    serializer_class = CitySerializer
    queryset = get_cities()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = CityFilters