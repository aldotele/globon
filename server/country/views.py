from django.http import JsonResponse
from .persistence import get_countries
from .serializers import CountrySerializer


def get_all_countries(request):
    all_countries = get_countries()
    serializer = CountrySerializer(all_countries, many=True)
    return JsonResponse(serializer.data, safe=False)
