import asyncio
import logging
import os

from django.apps import AppConfig

from .initializer import load_country_data


class InitializerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initializer'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            print("run_main")
            logging.info("ONE TIME EXECUTION: populating db ...")
            # import model
            from country.models import Country

            # check if countries are already on db or not
            if not Country.objects.all():
                print("empty tables")
                asyncio.run(load_country_data())

            return True
        else:
            print("no loading needed")
            pass
