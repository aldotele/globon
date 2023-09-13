from .models import City


def get_cities():
    return City.objects.all()