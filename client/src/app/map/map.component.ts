import { Component, AfterViewInit } from '@angular/core';
import {Map, Marker, Icon, TileLayer} from 'leaflet'
import { MarkerService } from '../marker.service';

const iconRetinaUrl = 'assets/marker-icon-2x.png';
const iconUrl = 'assets/marker-icon.png';
const shadowUrl = 'assets/marker-shadow.png';
const iconDefault = new Icon({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});
Marker.prototype.options.icon = iconDefault;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  private map;
  private selectedFilteringCriteria: string;
  minPopulation: any;
  maxPopulation: any;
  isFoundCountriesCountVisible: boolean = false;
  foundCountriesCount: number;
  isLoading: boolean = false;

	onSelected(value:string): void {
    this.isFoundCountriesCountVisible = false;
		this.selectedFilteringCriteria = value;
	}

  private initMap(): void {
    // initialize map and centering it
    this.map = new Map('map', {
      center: [39.8282, -18.5795],
      zoom: 1
    });

    // add tile layer
    const tiles = new TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
  }

  constructor(public markerService: MarkerService) {}

  ngAfterViewInit(): void {
    this.initMap();
  }

  onSubmit(form) {
    // filter countries based on search criteria and highlight them on map
    this.markerService.makeCountrySearchBorders(this.map, form.value);
    this.isLoading = true;

    // get the number of filtered countries
    this.markerService.foundCountries$.subscribe(foundCountriesCount => {
      this.foundCountriesCount = foundCountriesCount;
      this.isFoundCountriesCountVisible = true;
      this.isLoading = false;
    });
  }
}
