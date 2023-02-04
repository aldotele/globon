package persistence;

import com.mongodb.BasicDBList;
import com.mongodb.BasicDBObject;
import exception.SearchException;
import model.CountrySearch;
import org.jetbrains.annotations.NotNull;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import static util.RegexUtil.exactIgnoreCase;

public class QueryBuilder {
    private static final Map<String, String> incomeLevelToCode = Map.of(
            "high", "HIC",
            "upperMiddle", "UMC",
            "lowerMiddle", "LMC",
            "low", "LIC");

    @NotNull
    public static BasicDBList buildQueryConditions(CountrySearch search) throws SearchException {
        BasicDBList conditions = new BasicDBList();

        // population range
        BigDecimal maxPopulation = search.getMaxPopulation();
        if (maxPopulation != null) conditions.add(new BasicDBObject("population", new BasicDBObject("$lt", maxPopulation)));
        BigDecimal minPopulation = search.getMinPopulation();
        if (minPopulation != null) conditions.add(new BasicDBObject("population", new BasicDBObject("$gt", minPopulation)));

        // spoken languages
        List<String> languages = search.getLanguages();
        if (languages != null) {
            for (String language: languages) {
                conditions.add(new BasicDBObject("languages", exactIgnoreCase(language)));
            }
        }

        // borders
        List<String> borders = search.getBorders();
        if (borders != null) {
            for (String border: borders) conditions.add(new BasicDBObject("borders", border));
        }

        // name regex
        String nameRegex = search.getNameRegex();
        if (nameRegex != null) {
            Pattern namePattern = Pattern.compile(nameRegex, Pattern.CASE_INSENSITIVE);
            conditions.add(new BasicDBObject("name", new BasicDBObject("$regex", namePattern)));
        }

        // capital regex
        String capitalRegex = search.getCapitalRegex();
        if (capitalRegex != null) {
            Pattern capitalPattern = Pattern.compile(capitalRegex, Pattern.CASE_INSENSITIVE);
            conditions.add(new BasicDBObject("capital", new BasicDBObject("$regex", capitalPattern)));
        }

        // incomeLevel
        String incomeLevel = search.getIncomeLevel();
        if (incomeLevel != null && incomeLevelToCode.containsKey(incomeLevel)) {
            conditions.add(new BasicDBObject("incomeLevel.id", incomeLevelToCode.get(incomeLevel)));
        }

        if (conditions.isEmpty()) {
            throw new SearchException("at least one valid search criteria is needed.");
        }
        return conditions;
    }
}
