from rest_framework import serializers

from .models import Country, CountryGeography, CountrySociety, CountryEconomy


class CountryGeographySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Get the fields from the request context or from the kwargs
        fields = kwargs.pop('fields', None)

        # Call the super class initialization
        super(CountryGeographySerializer, self).__init__(*args, **kwargs)

        # If fields were provided, update the serializer's Meta fields
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = CountryGeography
        fields = ['country_id', 'maps', 'total_area_sq_km', 'land_area_sq_km', 'water_area_sq_km', 'coastline_length_km']


class CountryEconomySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Get the fields from the request context or from the kwargs
        fields = kwargs.pop('fields', None)

        # Call the super class initialization
        super(CountryEconomySerializer, self).__init__(*args, **kwargs)

        # If fields were provided, update the serializer's Meta fields
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = CountryEconomy
        fields = ['country_id', 'gdp_real', 'gdp_gross', 'gdp_agriculture', 'gdp_industry', 'gdp_services',
                  'real_gdp_growth_rate', 'real_gdp_per_capita', 'inflation_rate', 'industrial_production_growth_rate',
                  'labor_force', 'labor_force_agriculture', 'labor_force_industry', 'labor_force_services',
                  'unemployment_rate', 'unemployment_rate_youth', 'population_below_poverty_line', 'public_debt',
                  'taxes', 'exports', 'imports']


class CountrySocietySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Get the fields from the request context or from the kwargs
        fields = kwargs.pop('fields', None)

        # Call the super class initialization
        super(CountrySocietySerializer, self).__init__(*args, **kwargs)

        # If fields were provided, update the serializer's Meta fields
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = CountrySociety
        fields = ['country_id', 'languages', 'population', 'population_growth_rate', 'population_0_14_percentage',
                  'population_15_64_percentage', 'population_65_more_percentage', 'population_males_0_14',
                  'population_females_0_14', 'population_males_15_64', 'population_females_15_64', 'median_age',
                  'median_age_male', 'median_age_female', 'births_every_1000', 'deaths_every_1000',
                  'migrants_every_1000', 'urban_population_percentage', 'life_expectancy_at_birth',
                  'life_expectancy_at_birth_male', 'life_expectancy_at_birth_female', 'births_per_woman',
                  'health_expenditure', 'physicians_density', 'hospital_bed_density', 'obesity_rate',
                  'beer_consumption_per_capita', 'wine_consumption_per_capita','spirits_consumption_per_capita',
                  'tobacco_use', 'tobacco_use_male', 'tobacco_use_female', 'married_women_rate', 'literacy_rate',
                  'literacy_rate_male', 'literacy_rate_female']


class CountrySerializer(serializers.ModelSerializer):
    geography = CountryGeographySerializer(read_only=True)
    society = CountrySocietySerializer(read_only=True)
    economy = CountryEconomySerializer(read_only=True)

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
        fields = ['name', 'official_name', 'iso3', 'iso2', 'flag', 'capital', 'income_level',
                  'geography', 'society', 'economy']
