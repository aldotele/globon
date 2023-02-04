package proxy;

import com.fasterxml.jackson.core.type.TypeReference;
import com.mongodb.client.MongoCollection;
import model.Country;
import model.external.WorldBankCountryDetails;
import okhttp3.Request;
import okhttp3.Response;
import org.bson.Document;
import org.json.JSONArray;
import util.Api;
import util.SimpleClient;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

import static configuration.Configuration.mapper;
import static configuration.Configuration.simpleMapper;

public class WorldProxy {
    public static List<Country> retrieveAllCountries() throws IOException {
        Request request = SimpleClient.buildRequest(Api.External.REST_COUNTRIES_BASE_URL + "/all");
        Response response = SimpleClient.makeRequest(request);
        List<Country> allCountries = Arrays.asList(mapper.readValue(Objects.requireNonNull(response.body()).string(), Country[].class));
        return allCountries;
    }

    public static List<WorldBankCountryDetails> retrieveWorldBankCountriesData() throws IOException {
        Request worldBankRequest = SimpleClient.buildRequest(Api.External.WORLD_BANK_COUNTRY_API);
        Response worldBankResponse = SimpleClient.makeRequest(worldBankRequest);
        JSONArray jsonArray = new JSONArray(Objects.requireNonNull(worldBankResponse.body()).string());
        List<WorldBankCountryDetails> worldBankCountryDetails =
                simpleMapper.readValue(jsonArray.get(1).toString(), new TypeReference<>() {
                });
        return worldBankCountryDetails;
    }
}
