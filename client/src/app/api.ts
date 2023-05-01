import { environment } from "src/environments/environment";

export class Api {
    public static DOMAIN=environment.domain;
    public static COUNTRIES_BORDERS_GEOJSON = 'https://datahub.io/core/geo-countries/r/0.geojson';
 }