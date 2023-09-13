from django.db import models

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=255)
    city_ascii = models.CharField(max_length=255, null=True)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    admin_name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    population = models.BigIntegerField(null=True)
    sm_id = models.BigIntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city
