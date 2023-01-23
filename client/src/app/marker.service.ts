import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import * as L from 'leaflet';
import { AppSettings } from 'src/app.settings';
import fetch from 'node-fetch';

@Injectable({
  providedIn: 'root'
})
export class MarkerService {
  public countryDetails: string = "";
  countriesWithCoordinates: string = '/assets/data/countries_with_coordinates.geojson';

  constructor(private http: HttpClient) { }

  marker = L.geoJSON();

  myStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 0.65
  };

  makeCountrySearchBorders(map: L.Map, search: string): void {
    this.marker.clearLayers();
    let acronyms: string[];

    this.http.post(AppSettings.SERVER_URL + "/country/search?onlyAcronym=true", search).subscribe((res: string[]) => {
      // the result of the request is a list of country codes
      acronyms = res;

      this.http.get(this.countriesWithCoordinates).subscribe((resWithCoordinates: any) => {
        resWithCoordinates.forEach((country) => {
          // filtering countries by the codes returned in the previous request
          if (acronyms.includes(country.properties.ISO_A3)) {
            this.marker.addData(country).setStyle(this.myStyle).addTo(map)
            .on('click', onClickGetCountryDetails);
          }
        })
      })
    })
  }

  makeCountrySearchMarkers(map: L.Map, search: string): void {
    this.marker.clearLayers();
    this.http.post(AppSettings.SERVER_URL + "/country/search", search).subscribe((res:any) => {
      res.forEach((country) => {
        if (country.location != null) {
          this.marker.addData(country.location).addTo(map);
        }
      })
    })
  }

  public getCountryDetail() {
    return this.countryDetails;
  }
}

async function onClickGetCountryDetails(e) {
  let countryCode = e.layer.feature.properties.ISO_A3;

  const response = await fetch(AppSettings.SERVER_URL + "/country/code/" + countryCode);
  const data = await response.json();
  alert(data.name);

  // TODO display country details on browser, using 
  //console.log(data);
}



