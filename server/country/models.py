from django.db import models
import uuid


class Country(models.Model):
    uuid = models.UUIDField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=3)
    population = models.IntegerField()
    flag = models.URLField()
    capital = models.JSONField(null=True)
    translations = models.JSONField(null=True)
    currencies = models.JSONField(null=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def from_json(self, json):
        try:
            self.uuid = uuid.uuid4()
            self.name = json['name']['common']
            self.official_name = json['name']['official']
            self.acronym = json['cca3']
            self.population = json['population']
            self.flag = json['flags']['png']
            self.capital = json['capital']
            self.translations = Country.retrieve_translations(json['translations'])
            self.currencies = Country.retrieve_currencies(json['currencies'])
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
            currencies.append(value['name'] + " (" + value['symbol'] + ")")
        return currencies
