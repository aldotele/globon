from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=3)
    capital = models.CharField(max_length=255)
    population = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def from_json(self, json):
        try:
            self.name = json['name']['common']
            self.official_name = json['name']['official']
            self.acronym = json['cca3']
            self.capital = json['capital']
            self.population = json['population']
        except KeyError:
            pass
