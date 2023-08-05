<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import L, { marker } from 'leaflet';
import { Map, TileLayer } from 'leaflet';

const props = defineProps({
  iso3Codes: Array,
  searchCount: Number
})

const counter = computed(() => props.searchCount);

// deep property set to true allows to track nested properties changes also
watch(counter, () => {
  //console.log("new search: ", counter.value)
  //console.log(props.iso3Codes.length);
  // clearing borders when a new search is made
  state.marker.clearLayers();
  // fetching data again
  fetchData();
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
  //layerControlInstance: null
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

// fetch data
async function fetchData() {
  // api of all world countries borders coordinates
  const COUNTRIES_BORDERS = import.meta.env.VITE_COUNTRIES_BORDERS_GEOJSON;
  const response = await fetch(COUNTRIES_BORDERS, { method: 'GET', redirect: 'follow'});
  state.geoJsonData = await response.json();
  state.geoJsonData.features.forEach((geoJsonCountry) => {
    if (props.iso3Codes.includes(geoJsonCountry.properties.ISO_A3)) {
      applyBorders(geoJsonCountry);
    }
  })
}

function applyBorders(geoJsonBorders) {
  state.marker.addData(geoJsonBorders)
    .setStyle(myStyle)
    .addTo(state.mapInstance);
}


async function main() {
  
  await initMap();
  await fetchData();
}


onMounted(() => {
  console.log("search number ", counter.value);
  //console.log(props.iso3Codes)
  main();
})

</script>

<template>
  <main>
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

#leaflet-map {
  height: 98vh;
  width: 90%;
  overflow: hidden;
  margin: 0 auto;
  border-style: double;
}
</style>