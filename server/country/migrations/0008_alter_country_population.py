# Generated by Django 3.2.18 on 2023-10-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0007_auto_20231015_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='population',
            field=models.BigIntegerField(null=True),
        ),
    ]
