import itertools


def get_all_countries():
    from country.models import Country

    return Country.objects.all()


def get_all_languages():
    from country.models import Country

    sub_lists = list(Country.objects.values_list('languages', flat=True).distinct())
    list_with_duplicates = itertools.chain.from_iterable(sub_lists)
    unique_ist = list(dict.fromkeys(list_with_duplicates))
    unique_ist.sort()
    return unique_ist



