import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import { MarkerService } from '../marker.service';

const iconRetinaUrl = 'assets/marker-icon-2x.png';
const iconUrl = 'assets/marker-icon.png';
const shadowUrl = 'assets/marker-shadow.png';
const iconDefault = L.icon({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = iconDefault;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  private map;
  private selectedLocate = '';

	onSelected(value:string): void {
		this.selectedLocate = value;
	}

  private initMap(): void {
    // initialize map and centering it
    this.map = L.map('map', {
      center: [39.8282, -18.5795],
      zoom: 1
    });

    // add tile layer
    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
  }

  constructor(private markerService: MarkerService) {}

  ngAfterViewInit(): void {
    this.initMap();
  }

  onSubmit(contactForm) {
    if (this.selectedLocate == "marker") {
      this.markerService.makeCountrySearchMarkers(this.map, contactForm.value);
    } else {
      this.markerService.makeCountrySearchBorders(this.map, contactForm.value);
    }
  }
}
