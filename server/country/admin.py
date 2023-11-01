from django.contrib import admin

from .models import Country, CountryCodes, CountryBorder, CountrySociety, CountryGeography

# Register your models here.
admin.site.register(Country)
admin.site.register(CountryCodes)
admin.site.register(CountryBorder)
admin.site.register(CountrySociety)
admin.site.register(CountryGeography)
