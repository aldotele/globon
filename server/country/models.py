from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255, null=True)
    iso3 = models.CharField(max_length=3)
    flag = models.URLField(max_length=200, null=True)
    capital = models.JSONField(null=True)
    translations = models.JSONField(null=True)
    currencies = models.JSONField(null=True)
    map = models.URLField(max_length=200, null=True)
    income_level = models.CharField(max_length=4, null=True)

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class CountryCodes(models.Model):
    name = models.CharField(max_length=255)
    gec = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    stanag = models.CharField(max_length=3)
    internet = models.CharField(max_length=3)

    class Meta:
        db_table = 'country_codes'

    def __str__(self):
        return self.name


class CountryGeography(models.Model):
    iso3 = models.CharField(max_length=3)
    lat_lng = models.JSONField(null=True)
    total_area_sq_km = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    land_area_sq_km = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    water_area_sq_km = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    border_length_km = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    coastline_length_km = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    highest_point = models.JSONField(null=True)

    class Meta:
        db_table = 'country_geography'

    def __str__(self):
        return self.iso3


class CountryBorder(models.Model):
    country1 = models.CharField(max_length=255, null=True)
    country2 = models.CharField(max_length=255, null=True)
    length_km = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'country_border'

    def __str__(self):
        return str(self.country1) + "-" + str(self.country2)


class CountrySociety(models.Model):
    iso3 = models.CharField(max_length=3)
    languages = models.JSONField(null=True)
    population = models.BigIntegerField(null=True)
    population_growth_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    population_0_14_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    population_15_64_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    population_65_more_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    population_males_0_14 = models.BigIntegerField(null=True)
    population_females_0_14 = models.BigIntegerField(null=True)
    population_males_15_64 = models.BigIntegerField(null=True)
    population_females_15_64 = models.BigIntegerField(null=True)
    population_males_65_more = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    population_females_65_more = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    median_age = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    median_age_male = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    median_age_female = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    births_every_1000 = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="births every 1000 population")
    deaths_every_1000 = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="deaths every 1000 population")
    migrants_every_1000 = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="migrants every 1000 population")
    urban_population_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    life_expectancy_at_birth = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    life_expectancy_at_birth_male = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    life_expectancy_at_birth_female = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    births_per_woman = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="children born/woman")
    health_expenditure = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="as a percentage of GDP")
    physicians_density = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="physicians every 1000 population")
    hospital_bed_density = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="beds every 1000 population")
    obesity_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    alcohol_consumption_per_capita = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="liters")
    beer_consumption_per_capita = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="liters")
    wine_consumption_per_capita = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="liters")
    spirits_consumption_per_capita = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="liters")
    tobacco_use = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    tobacco_use_male = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    tobacco_use_female = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    married_women_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="ages 15-49")
    literacy_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    literacy_rate_male = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    literacy_rate_female = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")

    class Meta:
        db_table = 'country_society'

    def __str__(self):
        return self.iso3


class CountryEconomy(models.Model):
    iso3 = models.CharField(max_length=3)
    gdp_real = models.BigIntegerField(null=True, help_text="purchasing power parity in billion dollars")
    gdp_gross = models.BigIntegerField(null=True, help_text="in billion dollars")
    gdp_agriculture = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of total GDP")
    gdp_industry = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of total GDP")
    gdp_services = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of total GDP")
    real_gdp_growth_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    real_gdp_per_capita = models.BigIntegerField(null=True, help_text="in dollars")
    inflation_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    industrial_production_growth_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    labor_force = models.BigIntegerField(null=True)
    labor_force_agriculture = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    labor_force_industry = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    labor_force_services = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    unemployment_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    unemployment_rate_youth = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of unemployment 15-24")
    population_below_poverty_line = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage")
    public_debt = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of GDP")
    taxes = models.DecimalField(null=True, max_digits=5, decimal_places=2, help_text="percentage of GDP")
    exports = models.BigIntegerField(null=True, help_text="in billion dollars")
    imports = models.BigIntegerField(null=True, help_text="in billion dollars")

    class Meta:
        db_table = 'country_economy'

    def __str__(self):
        return self.iso3

