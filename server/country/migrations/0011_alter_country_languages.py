# Generated by Django 3.2.18 on 2023-05-06 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0010_alter_country_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='languages',
            field=models.JSONField(default=list),
        ),
    ]
