from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255, null=True)
    iso3 = models.CharField(max_length=3)
    population = models.BigIntegerField(null=True)
    flag = models.URLField(max_length=200, null=True)
    capital = models.JSONField(null=True)
    translations = models.JSONField(null=True)
    currencies = models.JSONField(null=True)
    map = models.URLField(max_length=200, null=True)
    languages = models.JSONField(null=True)
    borders = models.JSONField(null=True)
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
