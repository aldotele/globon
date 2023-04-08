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
        except KeyError:
            pass
