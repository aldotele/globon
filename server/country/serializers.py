from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Get the fields from the request context or from the kwargs
        fields = kwargs.pop('fields', None)

        # Call the super class initialization
        super(CountrySerializer, self).__init__(*args, **kwargs)

        # If fields were provided, update the serializer's Meta fields
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Country
        fields = ['name', 'official_name', 'iso3', 'iso2', 'flag', 'capital', 'translations',
                  'currencies', 'income_level']
