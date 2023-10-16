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
            logging.info("ONE TIME EXECUTION: populating db ...")
            # import model
            from country.models import Country

            # check if countries are already on db or not
            if Country.objects.all():
                logging.info("countries are already on db")
            else:
                asyncio.run(load_country_data())


            # check if countries are already on db or not
            # if Country.objects.all():
            #     logging.info("countries are already on db")
            # else:
            #     # invoke proxy to populate db
            #     all_countries = proxy.retrieve_all_countries()
            #     for country_in_json in all_countries:
            #         country = Country()
            #         country.from_json(country_in_json)
            #         country.save()
            #     logging.info("db populate with countries")
            #     world_bank_countries_details = proxy.retrieve_world_bank_country_details()
            #     for country_details in world_bank_countries_details:
            #         Country.objects.filter(iso3=country_details["id"]).update(income_level=country_details["incomeLevel"]["id"])
            return True
        else:
            pass
