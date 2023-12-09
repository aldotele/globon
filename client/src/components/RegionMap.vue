<script setup>
import { reactive, onMounted, watch, computed, ref } from 'vue'
import L from 'leaflet';
import Swal from 'sweetalert2';

const props = defineProps({
  searchCount: Number,
  filters: Object
})

const counter = computed(() => props.searchCount);
const regionChange = computed(() => props.filters.region);

// whenever a new region is selected without submitting a new search, the found flag is reset to zero to start clean
watch(regionChange, async () => {
  await clearBorders();
  state.foundRegionFlag = false;
})

// a new search will increment the counter, therefore previous markers will be removed first
watch(counter, async () => {
  await clearBorders();
  // clear also the found cities description
  state.foundRegionFlag = false;
  // fetching data again
  drawRegion();
})

const mapStyle = {
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
  foundRegionFlag: false,
  loadingRegion: false,
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

async function clearBorders() {
  state.marker.clearLayers();
}

// fetch data
async function drawRegion() {
  // loading spinner activated
  state.loadingRegion = true;
  let noRegionFilter = "";
  let REGIONS_API = `https://nominatim.openstreetmap.org/search.php?country=${props.filters.iso2}&state=${props.filters.region?props.filters.region:noRegionFilter}&polygon_geojson=1&format=jsonv2`;
  let response = await fetch(REGIONS_API, { method: 'GET', redirect: 'follow'});
  let responseBody = await response.json()
  if (responseBody && responseBody.length == 1 && "geojson" in responseBody[0] && "lat" in responseBody[0] && "lon" in responseBody[0]) {
    // update the center of the map to the region
    let lat = responseBody[0].lat;
    let lon = responseBody[0].lon;
    state.mapInstance.setView(new L.LatLng(lat, lon), 5);
    // found region flag
    state.foundRegionFlag = true;
    let geojson = responseBody[0].geojson;
    //console.log(geojson)
    state.marker.addData(geojson)
        .setStyle(mapStyle)
        .addTo(state.mapInstance);
    // deactivate spinner after region was found   
    state.loadingRegion = false;
  } else {
    // reset to world center
    state.mapInstance.setView(state.mapOptions.center, 3);
    // deactivate spinner when nothing was found
    state.loadingRegion = false;
  }
}

async function main() {
  await initMap();
  await drawRegion();
}

onMounted(() => {
  console.log("search number ", counter.value);
  main();
})
</script>


<template>
    <p>{{props.regions}}</p>
    <p>{{props.filters.iso3}}</p>

    <main>
      <div>
        <p v-if="state.loadingRegion" id="loading">Loading ...</p>
        <p v-if="!state.loadingRegion && state.foundRegionFlag && props.filters.region">{{ props.filters.region }} found</p>
      </div>
    <div :id="state.mapId"></div>
  </main>
</template>

<style lang="scss" scoped>
@import 'leaflet/dist/leaflet.css';
  
main {
  margin: 100px auto 30px auto;
}

p {
  text-align: center;
  font-size: large;
}

#leaflet-map {
  height: 98vh;
  width: 95%;
  overflow: hidden;
  margin: 0 auto;
  border-style: double;
}

</style>