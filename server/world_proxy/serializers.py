from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    expected = serializers.Field(source='actual')

    class Meta:
        model = Country
        fields = ('field1', 'field2', 'expected')