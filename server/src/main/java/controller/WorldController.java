package controller;

import configuration.Configuration;
import io.javalin.http.Handler;
import io.javalin.openapi.*;
import model.City;
import model.Country;
import model.CountrySearch;
import service.WorldService;
import util.Api;

import java.util.List;

public class WorldController {
    private static final WorldService worldService = WorldService.getInstance();

    @OpenApi(summary = "Get a list of all world countries", path = Api.Internal.ALL_COUNTRIES)
    public static Handler fetchAllCountries = ctx -> {
        List<Country> countries = worldService.retrieveAllCountries();
        ctx.json(countries);
    };

    @OpenApi(summary = "Get single country details", path = Api.Internal.COUNTRY_DETAILS,
            pathParams = @OpenApiParam(name = "name", description = "country name", required = true))
    public static Handler fetchCountryByName = ctx -> {
        String name = ctx.pathParam("name");
        Country country = worldService.retrieveCountryByName(name);
        ctx.json(country);
    };

    @OpenApi(summary = "Get single country details", path = Api.Internal.COUNTRY_DETAILS_BY_CODE,
            pathParams = @OpenApiParam(name = "code", description = "country code", required = true))
    public static Handler fetchCountryByCode = ctx -> {
        String code = ctx.pathParam("code").toUpperCase();
        Country country = worldService.fetchCountryByCode(code);
        ctx.json(country);
    };

    @OpenApi(summary = "get countries by search criteria", path = Api.Internal.COUNTRY_SEARCH, methods = HttpMethod.POST,
            requestBody = @OpenApiRequestBody(content = {@OpenApiContent(from = CountrySearch.class)}))
    public static Handler fetchCountriesBySearchCriteria = ctx -> {
        String body = ctx.body();
        CountrySearch search = Configuration.simpleMapper.readValue(body, CountrySearch.class);
        Boolean onlyAcronym = Boolean.valueOf(ctx.queryParam("onlyAcronym"));
        if (onlyAcronym) {
            List<String> acronyms = worldService.retrieveCountriesAcronyms(search);
            ctx.json(acronyms);
        } else {
            List<Country> filtered = worldService.retrieveCountriesBySearchCriteria(search);
            ctx.json(filtered);
        }
    };

    @OpenApi(summary = "Get all world capitals", path = Api.Internal.WORLD_CAPITALS)
    public static Handler fetchCapitals = ctx -> {
        List<String> worldCapitals = worldService.retrieveCapitals();
        ctx.json(worldCapitals);
    };

    @OpenApi(summary = "Get all world languages", path = Api.Internal.WORLD_LANGUAGES)
    public static Handler fetchLanguages = ctx -> {
        List<String> worldLanguages = worldService.retrieveLanguages();
        ctx.json(worldLanguages);
    };

    @OpenApi(summary = "Get all world currencies", path = Api.Internal.WORLD_CURRENCIES)
    public static Handler fetchCurrencies = ctx -> {
        List<String> worldCurrencies = worldService.retrieveCurrencies();
        ctx.json(worldCurrencies);
    };

    @OpenApi(summary = "Get cities within a country", path = Api.Internal.CITY_BY_COUNTRY,
            pathParams = @OpenApiParam(name = "country", description = "country name", required = true))
    public static Handler fetchCitiesByCountry = ctx -> {
        String countryName = ctx.pathParam("country");
        ctx.json(worldService.retrieveCitiesByCountry(countryName));
    };

    @OpenApi(summary = "Get city details", path = Api.Internal.CITY_DETAILS,
            pathParams = @OpenApiParam(name = "name", description = "city name", required = true))
    public static Handler fetchCityByName = ctx -> {
        String cityName = ctx.pathParam("name");
        City city = worldService.retrieveCityDetails(cityName);
        ctx.json(city);
    };
}
