# Generated by Django 3.2.18 on 2023-10-12 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0004_city_sm_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelTable(
            name='city',
            table='city',
        ),
    ]
