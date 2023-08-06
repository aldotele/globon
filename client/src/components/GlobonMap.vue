<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import L, { marker } from 'leaflet';
import { Map, TileLayer } from 'leaflet';
import Swal from 'sweetalert2';


const props = defineProps({
  iso3Codes: Array,
  searchCount: Number
})

const counter = computed(() => props.searchCount);

// deep property set to true allows to track nested properties changes also
watch(counter, async () => {
  //console.log("new search: ", counter.value)
  //console.log(props.iso3Codes.length);
  // clearing borders when a new search is made
  await clearMarkers();
  // clear also the found countried description
  state.foundCountriesFlag = false;
  // fetching data again
  applyBorders();
}, {
  deep: true,
})

const myStyle = {
  "color": "#ff7800",
  "weight": 1.5,
  "opacity": 0.65
};

const state = reactive({
  mapId: 'leaflet-map',
  mapOptions: {
    center: L.latLng(30.378472, 14.970598),
    zoom: 1,
    //zoomControl: true,
    //zoomAnimation: false,
    // maxBounds: L.LatLngBounds(
    //   L.latLng(18.91619, -171.791110603),
    //   L.latLng(71.3577635769, -66.96466)
    // ),
    layers: [],
  },
  marker: L.geoJSON(),
  geoJsonData: null,
  mapInstance: null,
  //layerControlInstance: null,
  foundCountriesCount: 0,
  foundCountriesFlag: false
})

async function initMap() {
  const leafletMap = L.map(state.mapId, state.mapOptions);

  // add tile layer
  const tile = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    minZoom: 3,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(leafletMap);

  // Create the layer control and add it to the map:
  // state.layerControlInstance = L.control.layers({
  //     OpenStreetMap: tile,
  //   }).addTo(leafletMap);
  // Add an event listener to the map:
  // leafletMap.on('zoomstart', () => {
  //   console.log('ZOOM STARTED');
  // });
  state.mapInstance = leafletMap;
}

async function clearMarkers() {
  state.marker.clearLayers();
}

// fetch data
async function fetchAllGeoJsonBorders() {
  // api of all world countries borders coordinates
  const COUNTRIES_BORDERS = import.meta.env.VITE_COUNTRIES_BORDERS_GEOJSON;
  const response = await fetch(COUNTRIES_BORDERS, { method: 'GET', redirect: 'follow'});
  state.geoJsonData = await response.json();
}

async function applyBorders() {
  state.geoJsonData.features.forEach((geoJsonCountry) => {
    if (props.iso3Codes.includes(geoJsonCountry.properties.ISO_A3)) {
      state.marker.addData(geoJsonCountry)
        .setStyle(myStyle)
        .addTo(state.mapInstance)
        .on('click', showCountryDetails);    
      }
  })
  state.foundCountriesCount = props.iso3Codes.length;
  state.foundCountriesFlag = true;
}

async function showCountryDetails(e) {
  let isoCode = e.layer.feature.properties.ISO_A3;
  const response = await fetch(import.meta.env.VITE_SERVER_ADDRESS + "/api/countries?isoCode=" + isoCode);
  const countriesByIsoCode = await response.json();
  if (countriesByIsoCode.length > 0) {
    triggerCountryAlert(countriesByIsoCode[0]);
  }
}

async function triggerCountryAlert(data) {
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

async function main() {
  await initMap();
  await fetchAllGeoJsonBorders();
  await applyBorders();
}

onMounted(() => {
  console.log("search number ", counter.value);
  //console.log(props.iso3Codes)
  main();
})

</script>

<template>
  <main>
    <!-- loading spinner & countries found information -->
    <div>
      <p v-if="state.foundCountriesFlag" id="foundCountriesCount">{{ state.foundCountriesCount }} countries were found</p>
      <p v-else id="loading">Loading Countries ...</p>
    </div>
    <div :id="state.mapId"></div>
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

p {
  text-align: center;
}

#leaflet-map {
  height: 98vh;
  width: 90%;
  overflow: hidden;
  margin: 0 auto;
  border-style: double;
}

</style>