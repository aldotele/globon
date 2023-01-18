package model.external;

import lombok.Data;

import java.util.List;

@Data
public class CountryCitiesExternalResponse {
    private Boolean error;
    private String msg;
    private List<String> data;
}

