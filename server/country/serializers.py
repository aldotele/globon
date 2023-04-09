from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['uuid', 'name', 'official_name', 'acronym', 'population', 'flag', 'capital', 'translations',
                  'currencies', 'map', 'languages']
