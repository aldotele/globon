import asyncio
import logging
import os

from django.apps import AppConfig

from initializer.initializer import load_countries


class InitializerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initializer'

    def ready(self):
        if os.environ.get('INITIALIZER'):
            logging.info("ONE TIME EXECUTION: populating db ...")
            # import model
            from country.models import Country
            # check if countries are already on db or not
            if not Country.objects.all():
                asyncio.run(load_countries())

            return True
        else:
            pass
