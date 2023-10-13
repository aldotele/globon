from django.db import models


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
        db_table = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.city
