import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import * as L from 'leaflet';
import { mapTo } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MarkerService {

  allcountries: string = '/assets/data/allcountries.geojson';
  usacapitals: string = '/assets/data/usa-capitals.geojson';
  coordinates: string = '/assets/data/coordinates.geojson';


  constructor(private http: HttpClient) { }

  marker = L.geoJSON();

  myStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 0.65
  };

  makeCountryBorders(map: L.Map, search: string): void {
    this.marker.clearLayers();
    let acronyms: string[];

    this.http.post("http://localhost:7070/country/search?onlyAcronym=true", search).subscribe((res: string[]) => {
      acronyms = res;

      this.http.get(this.coordinates).subscribe((coordinatesRes: any) => {
        coordinatesRes.forEach((country) => {
          if (acronyms.includes(country.properties.ISO_A3)) {
            this.marker.addData(country).setStyle(this.myStyle).addTo(map);
          }
        })  
      })
    })
  }


  makeCountryBordersPOC(map: L.Map): void {
    this.marker.clearLayers();
    this.http.get(this.coordinates).subscribe((res:any) => {
      res.forEach((feature) => {
        if (feature.properties.ADMIN == "Spain" || feature.properties.ADMIN == "Italy" || feature.properties.ADMIN == "China"
        || feature.properties.ADMIN == "United Kingdom" || feature.properties.ADMIN == "Luxembourg"
        || feature.properties.ADMIN == "Turkey" || feature.properties.ADMIN == "Belgium") {
          L.geoJSON(feature, {
            style: this.myStyle
          }).addTo(map);
        }
      })


      // L.geoJSON(res, {
      //   style: this.myStyle
      // }).addTo(map);
    })
  }

  makeCountrySearchMarkersPOC(map: L.Map, search: string): void {
    this.marker.clearLayers();
    this.http.post("http://localhost:7070/country/search", search).subscribe((res:any) => {
      res.forEach((element) => {
        if (element.location != null) {
          this.marker.addData(element.location).addTo(map);
        }
      })
    })
  }

  makeCountriesMarkersPOC(map: L.Map): void {
    this.http.get("http://localhost:7070/country/all").subscribe((res: any) => {
      res.forEach( (element) => {
        const marker = L.geoJSON(element.location).addTo(map);
      })
    })
  }

  makeCountryMarkerPOC(map: L.Map, countryName: string): void {
    this.http.get("http://localhost:7070/country/" + countryName).subscribe((res: any) => {
      const marker = L.geoJSON(res.location).addTo(map);
    })
  }

  makeCountryMarkers(map: L.Map): void {


    this.http.get(this.allcountries).subscribe((res: any) => {
      res.forEach( (element) => {
        const marker = L.geoJSON(element.location).addTo(map);
      });
    });
  }

  makeCapitalCircleMarkers(map: L.Map): void {
    this.http.get(this.usacapitals).subscribe((res: any) => {
      for (const c of res.features) {
        const lon = c.geometry.coordinates[0];
        const lat = c.geometry.coordinates[1];
        const circle = L.circleMarker([lat, lon]);
        
        circle.addTo(map);
      }
    });
  }
}
