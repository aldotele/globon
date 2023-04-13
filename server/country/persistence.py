from .models import Country


def get_countries():
    return Country.objects.all()


def get_country_by_code(code):
    return Country.objects.get(acronym=code)
