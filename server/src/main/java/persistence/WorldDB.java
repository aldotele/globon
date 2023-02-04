package persistence;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.google.gson.Gson;
import com.mongodb.BasicDBList;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Projections;
import exception.NotFoundException;
import exception.SearchException;
import lombok.extern.slf4j.Slf4j;
import model.Country;
import model.CountrySearch;
import org.bson.Document;
import proxy.WorldProxy;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static configuration.Configuration.ENV;
import static configuration.Configuration.simpleMapper;

@Slf4j
public class WorldDB {
    static String DB_NAME = "world";
    static MongoClient mongoClient;
    static MongoDatabase database;

    private static class Collection {
        private static final String COUNTRIES = "countries";
    }

    static {
        // when launching docker compose, db host will be mongo, otherwise localhost
        mongoClient = new MongoClient(Optional.ofNullable(ENV.get("MONGO_HOST")).orElse("localhost"), 27017);
        database = mongoClient.getDatabase(DB_NAME);
    }

    public static void init() throws JsonMappingException, JsonProcessingException, IOException {
        // retrieving all countries and writing to collection
        WorldDB.createCollection("countries");
        WorldDB.writeManyToCollection("countries", WorldProxy.retrieveAllCountries());
        // retrieving income levels and aggregating in existing collection
        MongoCollection<Document> collection = database.getCollection("countries");
        WorldProxy.retrieveWorldBankCountriesData()
                .forEach(country -> collection.updateOne(
                                new BasicDBObject("acronym", new BasicDBObject("$eq", country.getId())),
                                new BasicDBObject("$set", new BasicDBObject("incomeLevel", country.getIncomeLevel()))
                        )
                );
    }

    public static <T> void writeManyToCollection(String collectionName, List<T> objects) {
        MongoCollection<Document> collection = database.getCollection(collectionName);
        List<Document> documents = new ArrayList<>();
        Gson gson = new Gson();
        objects.forEach(obj -> {
            documents.add(Document.parse(gson.toJson(obj)));
            // ALTERNATIVE USING OBJECT MAPPER
            /*
            try {
                documents.add(Document.parse(objectMapper.writeValueAsString(country)));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            */
        });
        collection.insertMany(documents);
    }

    public static void createCollection(String collectionName) {
        try {
            // if the collection exists, clean it to start fresh
            database.getCollection(collectionName).drop();
            database.createCollection(collectionName);
            log.info("Collection " + collectionName + " created successfully");
        }
        catch (Exception e) {
            log.error("Failed at creating collection " + collectionName);
            log.error(e.getMessage());
        }
    }

    /**
     * retrieves all world countries
     */
    public static List<Country> retrieveCountries() throws JsonProcessingException {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        ArrayList<String> found = collection.find().projection(Projections.excludeId())
                .map(Document::toJson)
                .into(new ArrayList<>());
        List<Country> allCountries = simpleMapper.readValue(found.toString(), new TypeReference<>(){});
        return allCountries;
    }

    /**
     * retrieves a country by name
     */
    public static Country retrieveCountry(String countryName) throws JsonProcessingException, NotFoundException {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        String countryNameCapitalized = countryName.substring(0, 1).toUpperCase() +
                countryName.substring(1).toLowerCase();
        // retrieving the country from whatever language
        // TODO handle case of name with multiple words
        Document document = collection.find(new BasicDBObject("translations", countryNameCapitalized))
                .projection(Projections.excludeId()).first();
        if (document != null) {
            Country country = simpleMapper.readValue(document.toJson(), Country.class);
            return country;
        }
        throw new NotFoundException(countryName);
    }

    /**
     * retrieves a country by name
     */
    public static Country retrieveCountryByCode(String code) throws JsonProcessingException, NotFoundException {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        Document document = collection.find(new BasicDBObject("acronym", code))
                .projection(Projections.excludeId()).first();
        if (document != null) {
            Country country = simpleMapper.readValue(document.toJson(), Country.class);
            return country;
        }
        throw new NotFoundException(code);
    }

    /**
     * retrieves all countries that match the filter criteria
     */
    public static List<Country> retrieveCountries(CountrySearch search) throws JsonProcessingException, SearchException {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        BasicDBList conditions = QueryBuilder.buildQueryConditions(search);

        String queryResult = collection.find(new BasicDBObject("$and", conditions))
                .projection(Projections.excludeId())
                .map(Document::toJson)
                .into(new ArrayList<>())
                .toString();

        List<Country> allCountries = simpleMapper.readValue(queryResult, new TypeReference<>(){});

        return allCountries;
    }

    /**
     * retrieves the list of iso2 codes of the countries that match the filter criteria
     */
    public static List<String> retrieveCountriesAcronyms(CountrySearch search) throws SearchException {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        BasicDBList conditions = QueryBuilder.buildQueryConditions(search);

        List<String> filtered = collection
                .distinct("acronym", String.class)
                .filter(new BasicDBObject("$and", conditions))
                .into(new ArrayList<>());

        return filtered;
    }

    /**
     * retrieves the english country name
     */
    public static String retrieveEnglishCountryName(String countryName) {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        String countryNameCapitalized = countryName.substring(0, 1).toUpperCase() +
                countryName.substring(1).toLowerCase();
        Document document = collection.find(new BasicDBObject("translations", countryNameCapitalized)).first();
        if (document != null) {
            return document.get("name").toString();
        }
        return null;
    }

    /**
     * retrieves all the languages spoken in the world
     */
    public static List<String> retrieveLanguages() {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        return collection.distinct("languages", String.class)
                .into(new ArrayList<>());
    }

    /**
     * retrieves all currencies of the world
     */
    public static List<String> retrieveCurrencies() {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        return collection.distinct("currencies", String.class)
                .into(new ArrayList<>());
    }

    /**
     * retrieves all capitals of the world
     */
    public static List<String> retrieveCapitals() {
        MongoCollection<Document> collection = database.getCollection(Collection.COUNTRIES);
        return collection.distinct("capital", String.class)
                .into(new ArrayList<>());
    }
}
