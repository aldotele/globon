package model.external;

import lombok.Data;

import java.util.Map;

@Data
public class WorldBankCountryDetails {
    private String id;
    private String iso2Code;
    private String name;
    private Map<String, String> region;
    private Map<String, String> adminRegion;
    private Map<String, String> incomeLevel;
    private Map<String, String> lendingType;
    private String capitalCity;
    private String longitude;
    private String latitude;
}
