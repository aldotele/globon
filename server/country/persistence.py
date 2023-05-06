from .models import Country
import itertools


def get_countries():
    return Country.objects.all()


def get_country_by_code(code):
    return Country.objects.get(acronym=code)


def get_all_languages():
    sub_lists = list(Country.objects.values_list('languages', flat=True).distinct())
    list_with_duplicates = itertools.chain.from_iterable(sub_lists)
    unique_ist = list(dict.fromkeys(list_with_duplicates))
    return unique_ist




