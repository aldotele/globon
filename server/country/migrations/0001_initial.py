# Generated by Django 3.2.18 on 2023-04-05 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('official_name', models.CharField(max_length=255)),
                ('acronym', models.CharField(max_length=3)),
                ('capital', models.CharField(max_length=255)),
                ('population', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
    ]
