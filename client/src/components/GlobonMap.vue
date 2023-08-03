<script>
import { ref } from 'vue'
import L from 'leaflet';
import { Map, TileLayer } from 'leaflet';

export default {
  name: 'GlobonMap',
  props: {
    iso3Codes: {
      type: Array,
    },
  },  data() {
    return {
      mapId: 'leaflet-map',
      mapOptions: {
        center: L.latLng(30.378472, 14.970598),
        zoom: 1,
        zoomControl: true,
        zoomAnimation: false,
        // maxBounds: L.LatLngBounds(
        //   L.latLng(18.91619, -171.791110603),
        //   L.latLng(71.3577635769, -66.96466)
        // ),
        layers: [],
      },
      marker: L.geoJSON(),
      geoJsonData: null,
      mapInstance: null,
      layerControlInstance: null
    };
  },
  // watch: { // It listens to the change in prop name
  //   iso3Codes: function () {
  //     console.log("changed"); // print out when the name changes
  //     if (newArr.length === 0) {
  //       console.log("here")
  //       this.marker.clearLayers();
  //     }
  //   },
  // },
  methods: {
    initMap() {
      const leafletMap = L.map(this.mapId, this.mapOptions);

      // add tile layer
      const tile = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        minZoom: 3,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(leafletMap);

      // Create the layer control and add it to the map:
      this.layerControlInstance = L.control.layers({
          OpenStreetMap: tile,
        }).addTo(leafletMap);
      // Add an event listener to the map:
      leafletMap.on('zoomstart', () => {
        console.log('ZOOM STARTED');
      });
      this.mapInstance = leafletMap;
    },
    // fetch data
    async fetchData() {
      console.log(this.iso3Codes)
      // api of all world countries borders coordinates
      const COUNTRIES_BORDERS = import.meta.env.VITE_COUNTRIES_BORDERS_GEOJSON;

      fetch(COUNTRIES_BORDERS, { method: 'GET', redirect: 'follow'})
        .then((response) => response.json())
        .then((geoJson) => geoJson.features.forEach((country) => {
          if (this.iso3Codes.includes(country.properties.ISO_A3)) {
            this.marker.addData(country).setStyle(this.myStyle)
              .addTo(this.mapInstance);
              //polygons.value.push(country)
          }
        }))
    }
  },
  mounted() {
    this.initMap();
    this.fetchData();
  },
};

const myStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 0.65
  };



// let zoom = ref(3)
// let center = ref([30, 15])

const polygons = ref([])

let polygon = ref([
  [14.8825666303934, 120.546442034957],
  [14.8824267931024, 120.546643906729],
  [14.8821802041235, 120.546473992789],
  [14.8821850816981, 120.546383823217],
  [14.8821860579818, 120.54636577501],
  [14.8821851472004, 120.546358612103],
  [14.8822835496028, 120.546237482133],
  [14.8825666303934, 120.546442034957],
]);

//polygons.value.push(polygon)
</script>

<template>
  <main>
    <div :id="mapId"></div>
  </main>
    <!-- <main>
      <l-map style="display:block" ref="map" v-model:zoom="zoom" v-model:center="center" :useGlobalLeaflet="false">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      layer-type="base"
                      name="Open Street Map">
        </l-tile-layer>
        <l-geo-json v-for="(polygon, index) in polygons" :key="index" :geojson="polygon" :style="{ color: 'red', fill: false }" /> -->
        <!-- <l-geo-json :geojson="geojson" :style="{ color: 'red', fill: false }" /> -->
        <!-- <l-polygon v-for="(polygon, index) in polygons" :key="index" :lat-lngs="polygon" color="red" :fill="false" /> -->
        <!-- {/* <l-polygon :lat-lngs="polygon" color="red" :fill="false" /> */} -->
      <!-- </l-map>
      
    </main> -->
</template>

<style lang="scss" scoped>
@import 'leaflet/dist/leaflet.css';
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;    
}
  
main {
  height: 60vh;
  width: 95vw;
  margin: 100px auto 30px auto;
}

#leaflet-map {
  height: 98vh;
  width: 90%;
  overflow: hidden;
  margin: 0 auto;
  border-style: double;
}
</style>