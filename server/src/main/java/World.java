import configuration.Configuration;
import controller.CityController;
import controller.CountryController;
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

        app.get(Api.Internal.ALL_COUNTRIES, CountryController.fetchAllCountries);

        // COUNTRY BY NAME
        app.get(Api.Internal.COUNTRY_DETAILS, CountryController.fetchCountryByName);

        //  COUNTRY FILTERS
        app.post(Api.Internal.COUNTRY_SEARCH, CountryController.fetchCountries);

        // ALL CITIES BY COUNTRY
        app.get("/city/in/{country}", CityController.fetchCitiesByCountry);

        // SINGLE CITY DETAILS
        app.get(Api.Internal.CITY_DETAILS, CityController.fetchCityByName);

        // WORLD LANGUAGES
        app.get("/world/languages", WorldController.fetchLanguages);

        // WORLD CURRENCIES
        app.get("/world/currencies", WorldController.fetchCurrencies);

        // WORLD CAPITALS
        app.get("/world/capitals", WorldController.fetchCapitals);
    }
}

