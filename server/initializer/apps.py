import asyncio
import logging

from django.apps import AppConfig

from .initializer import load_countries


class InitializerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'initializer'

    def ready(self):
        from country.models import Country

        logging.info("ONE TIME EXECUTION: populating db ...")
        asyncio.run(load_countries())

