package model;

import lombok.Data;

import java.math.BigDecimal;
import java.util.List;

@Data
public class CountrySearch {
    private String nameRegex;
    private String acronym;
    private String capitalRegex;
    private List<String> borders;
    private BigDecimal minPopulation;
    private BigDecimal maxPopulation;
    private List<String> continents;
    private List<String> languages;
}
