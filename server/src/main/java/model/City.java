package model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

import java.io.Serializable;
import java.math.BigDecimal;

@Accessors(chain = true)
@Data
public class City implements Serializable {
    @JsonProperty("name")
    private String name;
    @JsonProperty("latitude")
    private BigDecimal latitude;
    @JsonProperty("longitude")
    private BigDecimal longitude;
    @JsonProperty("country")
    private String country;
    @JsonProperty("population")
    private BigDecimal population;
    @JsonProperty("is_capital")
    private boolean isCapital;
}