from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.response import Response
from rest_framework.views import APIView

from city.models import City


class CountryRegionsList(APIView):
    def get(self, request, iso):
        # regions are retrieved by aggregating all distinct regions from cities table after filtering by country (iso)
        if len(iso) == 3:
            regions = City.objects.filter(iso3__iexact=iso).aggregate(arr=ArrayAgg("admin_name", distinct=True))
            return Response(regions['arr'])
        elif len(iso) == 2:
            regions = City.objects.filter(iso2__iexact=iso).aggregate(arr=ArrayAgg("admin_name", distinct=True))
            return Response(regions['arr'])
        else:
            raise Exception("iso not valid")
