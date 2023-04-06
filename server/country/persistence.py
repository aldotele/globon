from .models import Country


def get_countries():
    return Country.objects.all()
