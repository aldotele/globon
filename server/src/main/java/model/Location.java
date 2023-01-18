package model;

import lombok.Data;

import java.util.List;

@Data
public class Location {
    private String type;
    private List<String> coordinates;
}
