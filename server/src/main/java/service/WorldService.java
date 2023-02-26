package service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import exception.NotFoundException;
import exception.SearchException;
import model.City;
import model.Country;
import model.CountrySearch;
import model.external.CountryCitiesExternalResponse;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import persistence.WorldDB;
import util.Api;
import util.SimpleClient;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import static configuration.Configuration.*;

public class WorldService {
    public static WorldService instance = new WorldService();

    private WorldService() {
        // prevents external instantiation
    }

    public static WorldService getInstance() {
        return instance;
    }
    public List<Country> retrieveAllCountries() throws JsonProcessingException {
        return WorldDB.retrieveCountries();
    }

    public Country retrieveCountryByName(String name) throws NotFoundException, JsonProcessingException {
        return WorldDB.retrieveCountry(name);
    }

    public Country fetchCountryByCode(String code) throws NotFoundException, JsonProcessingException {
        return WorldDB.retrieveCountryByCode(code);
    }

    public List<String> retrieveCitiesByCountry(String countryName) throws NotFoundException, IOException {
        Country country = WorldDB.retrieveCountry(countryName);
        Request request = SimpleClient.buildRequest(Api.External.COUNTRIESNOW_BASE_URL + "/q?country=" + country.getName());
        Response response = SimpleClient.makeRequest(request);
        CountryCitiesExternalResponse mappedResponse = simpleMapper
                .readValue(Objects.requireNonNull(response.body()).string(), new TypeReference<>(){});
        List<String> countryCities = mappedResponse.getData();
        return countryCities;
    }

    public City retrieveCityDetails(String cityName) throws IOException, NotFoundException {
        String apiKey = ENV.get("NINJA_API_KEY");
        Map<String, String> headers = Map.of("x-api-key", Objects.requireNonNull(apiKey));
        String url = Api.External.API_NINJA_BASE_URL + "?name=" + cityName;
        Request request = SimpleClient.buildRequest(url, headers);
        Response response = SimpleClient.makeRequest(request);
        JSONArray jsonArray = new JSONArray(Objects.requireNonNull(response.body()).string());
        if (jsonArray.toList().isEmpty()) throw new NotFoundException(cityName);
        City city = mapper.readValue(jsonArray.get(0).toString(), City.class);
        return city;
    }

    public List<String> retrieveCountriesAcronyms(CountrySearch search) throws SearchException {
        return WorldDB.retrieveCountriesAcronyms(search);
    }

    public List<Country> retrieveCountriesBySearchCriteria(CountrySearch search) throws SearchException, JsonProcessingException {
        return WorldDB.retrieveCountries(search);
    }

    public List<String> retrieveLanguages() {
        return WorldDB.retrieveLanguages();
    }

    public List<String> retrieveCurrencies() {
        return WorldDB.retrieveCurrencies();
    }

    public List<String> retrieveCapitals() {
        return WorldDB.retrieveCapitals();
    }
}
