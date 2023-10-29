from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'official_name', 'iso3', 'population', 'flag', 'capital', 'translations',
                  'currencies', 'map', 'languages', 'borders', 'income_level']
