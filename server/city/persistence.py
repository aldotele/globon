from .models import City


def get_all_cities():
    return City.objects.all()
