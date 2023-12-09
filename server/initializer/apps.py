import asyncio
import logging
import os

from django.apps import AppConfig

from initializer.initializer import load_countries, oneTimeIso2Update


class InitializerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initializer'

    def ready(self):
        from country.models import Country
        oneTimeIso2Update()

        if os.environ.get('RUN_MAIN'):
            logging.info("ONE TIME EXECUTION: populating db ...")
            # import model

            # check if countries are already on db or not
            if not Country.objects.all():
                asyncio.run(load_countries())

            return True
        else:
            pass

