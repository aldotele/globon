# Generated by Django 3.2.18 on 2023-11-01 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0006_auto_20231101_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countrysociety',
            old_name='birth_every_1000',
            new_name='births_every_1000',
        ),
        migrations.RenameField(
            model_name='countrysociety',
            old_name='death_every_1000',
            new_name='deaths_every_1000',
        ),
    ]