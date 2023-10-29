import asyncio
import logging

from django.apps import AppConfig

from .initializer import load_country_data


class InitializerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initializer'

    def ready(self):
        #if os.environ.get('RUN_MAIN'):
            logging.info("ONE TIME EXECUTION: populating db ...")
            # import model
            from country.models import Country

            # check if countries are already on db or not
            if not Country.objects.all():
                asyncio.run(load_country_data())

            return True
        #else:
            pass
