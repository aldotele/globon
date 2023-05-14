from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['uuid', 'name', 'official_name', 'iso_code', 'population', 'flag', 'capital', 'translations',
                  'currencies', 'map', 'languages', 'borders', 'income_level']
