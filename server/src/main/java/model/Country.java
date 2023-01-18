package model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Data
public class Country implements Serializable {
    private String name;
    private String officialName;
    private String acronym;
    private String isoCode;
    private String capital;
    private List<String> borders;
    private String maps;
    private List<String> currencies;
    private BigDecimal population;
    private List<String> continents;
    private String flag;
    private List<String> languages;
    private List<String> translations;
    private Location location;

    @JsonProperty("cca2")
    private void retrieveIsoCode(String isoCode) {
        this.isoCode = isoCode;
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("name")
    private void retrieveName(Map<String,Object> name) {
        this.name = (String)name.get("common");
        this.officialName = (String)name.get("official");
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("capital")
    private void retrieveCapital(List<String> capital) {
        this.capital = capital.get(0);
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("borders")
    private void retrieveBorders(List<String> borders) {
        this.borders = borders;
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("maps")
    private void retrieveMaps(Map<String,Object> maps) {
        this.maps = (String)maps.get("googleMaps");
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("flags")
    private void retrieveFlag(Map<String,Object> flags) {
        this.flag = (String)flags.get("svg");
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("languages")
    private void retrieveLanguages(Map<String,String> languages) {
        this.languages = languages.values().stream().toList();
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("currencies")
    private void retrieveCurrencies(Map<String,Object> currencies) {
        List<String> output = new ArrayList<>();
        List<String> currencyKeys = currencies.keySet().stream().toList();
        for (String currencyKey: currencyKeys) {
            Map<String, String> inner = (Map<String, String>) currencies.get(currencyKey);
            output.add(inner.get("name") + " " + "(" + inner.get("symbol") + ")");
        }
        this.currencies = output;
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("cca3")
    private void retrieveShortName(String acronym) {
        this.acronym = acronym;
    }

    @JsonProperty("translations")
    private void retrieveTranslations(Map<String,Object> translations) {
        List<String> translationKeys = translations.keySet().stream().toList();
        List<String> output = new ArrayList<>();
        for (String translationKey: translationKeys) {
            Map<String, String> inner = (Map<String, String>) translations.get(translationKey);
            output.add(inner.get("common"));
        }
        this.translations = output;
    }
}

