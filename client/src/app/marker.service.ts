import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import * as L from 'leaflet';
import { Api } from 'src/app/api';
import fetch from 'node-fetch';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class MarkerService {
  public countryDetails: string = "";

  constructor(private http: HttpClient) { }

  marker = L.geoJSON();

  myStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 0.65
  };

  makeCountrySearchBorders(map: L.Map, search: string): number {
    // clean map before new request
    this.marker.clearLayers();
    var foundCountries: number = 0;

    this.http.post(Api.SERVER + "/country/search?onlyAcronym=true", search).subscribe((countryCodes: string[]) => {
      // save the number of countries found, to be displayed as information
      foundCountries = countryCodes.length;

      this.http.get(Api.COUNTRIES_BORDERS_GEOJSON).subscribe((resWithCoordinates: any) => {
        resWithCoordinates.features.forEach((country) => {
          // filtering countries by the codes returned in the previous request
          if (countryCodes.includes(country.properties.ISO_A3)) {
            this.marker.addData(country).setStyle(this.myStyle).addTo(map)
            .on('click', onClickGetCountryDetails);
          }
        })
      })
    })
    return foundCountries;
  }

  makeCountrySearchMarkers(map: L.Map, search: string): void {
    this.marker.clearLayers();
    this.http.post(Api.SERVER + "/country/search", search).subscribe((res:any) => {
      res.forEach((country) => {
        if (country.location != null) {
          this.marker.addData(country.location).addTo(map)
          // TODO add logic
        }
      })
    })
  }
}

async function onClickGetCountryDetails(e) {
  let countryCode = e.layer.feature.properties.ISO_A3;
  const response = await fetch(Api.SERVER + "/country/code/" + countryCode);
  const data = await response.json();
  displayCountryDetails(data);
  // TODO consider using modal for displaying country details 
}

async function displayCountryDetails(data) {
  // triggering alert with country info
  Swal.fire({
    title: data.name,
    html: "<h3 style='font-weight:500'>" 
    + "<b>population</b>: " + data.population.toLocaleString() + "<br>" 
    + "<b>capital city</b>: " + data.capital + "<br>"
    + "<b>currencies</b>: " + data.currencies + "<br>"
    + "<b>spoken languages</b>: " + data.languages
    + "</h3>",
    showConfirmButton: false,
    showCancelButton: true,
    cancelButtonText: "Close"
  });
}



