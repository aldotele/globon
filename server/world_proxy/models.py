from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=3)
    capital = models.CharField(max_length=255)
    population = models.IntegerField

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name