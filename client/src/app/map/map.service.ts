import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import * as L from 'leaflet';
import { Api } from 'src/app/api';
import fetch from 'node-fetch';
import Swal from 'sweetalert2';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  private foundCountriesSubject = new Subject<number>();
  foundCountries$: Observable<number> = this.foundCountriesSubject.asObservable();

  constructor(private http: HttpClient) { }

  marker = L.geoJSON();

  myStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 0.65
  };

  makeCountrySearchBorders(map: L.Map, search: string): void {
    // clean map before new request
    this.marker.clearLayers();
    var foundCountriesCount: number;

    this.http.post(Api.SERVER + "/api/countries/", search).subscribe((countries: object[]) => {
      var acronyms = countries.map(obj => obj["acronym"]);
      // save the number of countries found, to be displayed as information
      foundCountriesCount = acronyms.length;
      this.http.get(Api.COUNTRIES_BORDERS_GEOJSON).subscribe((resWithCoordinates: any) => {
        resWithCoordinates.features.forEach((country) => {
          // filtering countries by the codes returned in the previous request
          if (acronyms.includes(country.properties.ISO_A3)) {
            this.marker.addData(country).setStyle(this.myStyle).addTo(map)
            .on('click', onClickGetCountryDetails);
          }
        });
        this.foundCountriesSubject.next(foundCountriesCount);
      });
    });
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
  const response = await fetch(Api.SERVER + "/api/countries/code/" + countryCode);
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



