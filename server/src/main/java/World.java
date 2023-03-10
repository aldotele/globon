import configuration.Configuration;
import controller.WorldController;
import exception.NotFoundException;
import exception.SearchException;
import io.javalin.Javalin;
import persistence.WorldDB;
import util.Api;

import java.io.IOException;
import java.util.List;


public class World {
    public static void main(String[] args) throws IOException {
        // invoke all countries and store them in MongoDB
        WorldDB.init();

        Javalin app = Javalin.create(Configuration.appConfig)
                .start(7070);

        // Exception handling
        List<Class<? extends Exception>> badRequestExceptions = List.of(NotFoundException.class, SearchException.class);
        badRequestExceptions.forEach(ex -> app.exception(ex, (e, ctx) -> {
            ctx.status(400);
            ctx.json(e.getMessage());
        }));

        // WELCOME
        app.get("/", context -> context.result("Welcome to World proxy"));

        // ALL COUNTRIES

        app.get(Api.Internal.ALL_COUNTRIES, WorldController.fetchAllCountries);

        // COUNTRY BY NAME
        app.get(Api.Internal.COUNTRY_DETAILS, WorldController.fetchCountryByName);

        // COUNTRY BY ISO3 CODE
        app.get(Api.Internal.COUNTRY_DETAILS_BY_CODE, WorldController.fetchCountryByCode);

        //  COUNTRY FILTERS
        app.post(Api.Internal.COUNTRY_SEARCH, WorldController.fetchCountriesBySearchCriteria);

        // ALL CITIES BY COUNTRY
        app.get(Api.Internal.CITY_BY_COUNTRY, WorldController.fetchCitiesByCountry);

        // SINGLE CITY DETAILS
        app.get(Api.Internal.CITY_DETAILS, WorldController.fetchCityByName);

        // WORLD LANGUAGES
        app.get(Api.Internal.WORLD_LANGUAGES, WorldController.fetchLanguages);

        // WORLD CURRENCIES
        app.get(Api.Internal.WORLD_CURRENCIES, WorldController.fetchCurrencies);

        // WORLD CAPITALS
        app.get(Api.Internal.WORLD_CAPITALS, WorldController.fetchCapitals);
    }
}

