from .persistence import get_countries
from .serializers import CountrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class CountryView(APIView):
    def get(self, request):
        queryset = get_countries().order_by('name')
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)

