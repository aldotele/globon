package controller;

import configuration.Configuration;
import io.javalin.http.Handler;
import io.javalin.openapi.*;
import model.Country;
import model.CountrySearch;
import persistence.WorldDB;
import util.Api;

import java.util.List;

public class CountryController {

    @OpenApi(summary = "Get a list of all world countries", path = Api.Internal.ALL_COUNTRIES)
    public static Handler fetchAllCountries = ctx -> {
        List<Country> countries = WorldDB.retrieveCountries();
        ctx.json(countries);
    };

    @OpenApi(summary = "Get single country details", path = Api.Internal.COUNTRY_DETAILS,
            pathParams = @OpenApiParam(name = "name", description = "country name", required = true))
    public static Handler fetchCountryByName = ctx -> {
        String name = ctx.pathParam("name");
        Country country = WorldDB.retrieveCountry(name);
        ctx.json(country);
    };

    @OpenApi(summary = "get countries with filter", path = Api.Internal.COUNTRY_SEARCH,
            methods = HttpMethod.POST,
            requestBody = @OpenApiRequestBody(
            content = {
                    @OpenApiContent(from = CountrySearch.class)
            }
    ))
    public static Handler fetchCountries = ctx -> {
      String body = ctx.body();
      CountrySearch search = Configuration.simpleMapper.readValue(body, CountrySearch.class);
        Boolean onlyAcronym = Boolean.valueOf(ctx.queryParam("onlyAcronym"));
        if (onlyAcronym) {
            List<String> acronyms = WorldDB.retrieveCountriesAcronyms(search);
            ctx.json(acronyms);
        } else {
            List<Country> filtered = WorldDB.retrieveCountries(search);
            ctx.json(filtered);
        }
    };
}
