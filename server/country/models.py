import uuid

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=3)
    population = models.BigIntegerField(null=True)
    flag = models.URLField(max_length=200, null=True)
    capital = models.JSONField(null=True)
    translations = models.JSONField(null=True)
    currencies = models.JSONField(null=True)
    map = models.URLField(max_length=200, null=True)
    languages = models.JSONField(default=list)
    borders = models.JSONField(null=True)
    income_level = models.CharField(max_length=4, null=True)

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name

    def from_json(self, json):
        try:
            self.uuid = uuid.uuid4()
            self.name = json['name']['common']
            self.official_name = json['name']['official']
            self.iso3 = json['cca3']
            self.population = json['population']
            self.flag = json['flags']['svg']
            self.capital = json['capital']
            self.translations = Country.retrieve_translations(json['translations'])
            self.currencies = Country.retrieve_currencies(json['currencies'])
            self.map = json['maps']['openStreetMaps']
            self.languages = Country.retrieve_languages(json['languages'])
            self.borders = json['borders']
        except KeyError:
            pass

    @staticmethod
    def retrieve_translations(json_node):
        translations = []
        for key, value in json_node.items():
            translation = value['common']
            if translation not in translations:
                translations.append(translation)
        return translations

    @staticmethod
    def retrieve_currencies(json_node):
        currencies = []
        for key, value in json_node.items():
            currency = value.get('name', "")
            if 'symbol' in value:
                currency += " (" + value['symbol'] + ")"
            currencies.append(currency)
        return currencies

    @staticmethod
    def retrieve_languages(json_node):
        languages = []
        for key, value in json_node.items():
            languages.append(value)
        return languages


class CountryCodes(models.Model):
    name = models.CharField(max_length=255)
    gec = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    stanag = models.CharField(max_length=3)
    internet = models.CharField(max_length=3)

    class Meta:
        db_table = 'country_codes'
