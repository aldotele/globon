package controller;

import com.fasterxml.jackson.core.type.TypeReference;
import exception.NotFoundException;
import io.javalin.http.Handler;
import io.javalin.openapi.OpenApi;
import io.javalin.openapi.OpenApiParam;
import model.City;
import model.Country;
import model.external.CountryCitiesExternalResponse;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import persistence.WorldDB;
import util.Api;
import util.SimpleClient;

import java.util.List;
import java.util.Map;
import java.util.Objects;

import static configuration.Configuration.*;

public class CityController {

    public static Handler fetchCitiesByCountry = ctx -> {
        String countryName = ctx.pathParam("country");
        Country country = WorldDB.retrieveCountry(countryName);
        Request request = SimpleClient.buildRequest(Api.External.COUNTRIESNOW_BASE_URL + "/q?country=" + country.getName());
        Response response = SimpleClient.makeRequest(request);
        CountryCitiesExternalResponse mappedResponse = simpleMapper
                .readValue(Objects.requireNonNull(response.body()).string(), new TypeReference<>(){});
        List<String> countryCities = mappedResponse.getData();
        ctx.json(countryCities);
    };

    @OpenApi(summary = "Get city details", path = Api.Internal.CITY_DETAILS,
            pathParams = @OpenApiParam(name = "name", description = "city name", required = true))
    public static Handler fetchCityByName = ctx -> {
        String apiKey = ENV.get("NINJA_API_KEY");
        Map<String, String> headers = Map.of("x-api-key", Objects.requireNonNull(apiKey));
        String cityName = ctx.pathParam("name");
        String url = Api.External.API_NINJA_BASE_URL + "?name=" + cityName;
        Request request = SimpleClient.buildRequest(url, headers);
        Response response = SimpleClient.makeRequest(request);
        JSONArray jsonArray = new JSONArray(Objects.requireNonNull(response.body()).string());

        if (jsonArray.toList().isEmpty()) throw new NotFoundException(cityName);

        City city = mapper.readValue(jsonArray.get(0).toString(), City.class);
        ctx.json(city);

    };

}