package util;

public class Api {
    public static class Internal {
        public static final String ALL_COUNTRIES = "/country/all";
        public static final String COUNTRY_DETAILS = "/country/{name}";
        public static final String COUNTRY_SEARCH = "/country/search";
        public static final String CITY_DETAILS = "/city/{name}";
    }

    public static class External {
        public static final String REST_COUNTRIES_BASE_URL = "https://restcountries.com/v3.1";
        public static final String COUNTRIESNOW_BASE_URL = "https://countriesnow.space/api/v0.1/countries/cities";
        public static final String API_NINJA_BASE_URL = "https://api.api-ninjas.com/v1/city";
        public static final String COUNTRY_CODES_COORDINATES_CSV = "https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv";
    }
}
