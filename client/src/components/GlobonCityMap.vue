<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import L, { marker } from 'leaflet';
import { Map, TileLayer } from 'leaflet';
import Swal from 'sweetalert2';


const props = defineProps({
  citiesCoords: Array,
  searchCount: Number
})

const counter = computed(() => props.searchCount);

// deep property set to true allows to track nested properties changes also
watch(counter, async () => {
  await clearMarkers();
  // clear also the found cities description
  state.foundCitiesFlag = false;
  // fetching data again
  applyMarkers();
}, {
  deep: true,
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
    layers: [],
  },
  mapInstance: null,
  markerGroup: null,
  foundCitiesCount: 0,
  foundCitiesFlag: false
})

async function initMap() {
  const leafletMap = L.map(state.mapId, state.mapOptions);

  // add tile layer
  const tile = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    minZoom: 3,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(leafletMap);

  state.mapInstance = leafletMap;
}

async function clearMarkers() {
  // deleting the group of markers related to the last search
  state.mapInstance.removeLayer(state.markerGroup);
}

async function applyMarkers() {
  // before applying markers, create a marker group for the current search
  state.markerGroup = L.layerGroup().addTo(state.mapInstance)
  props.citiesCoords.forEach((cityCoords) => {
    // creating a new marker with lat, lng and add it to the group
    const marker = L.marker(cityCoords);
    marker.addTo(state.markerGroup)
    .on('click', showCityDetails);
  })

  state.foundCitiesCount = props.citiesCoords.length;
  state.foundCitiesFlag = true;
}

async function showCityDetails(e) {
  console.log(e);

  // triggering alert with country info
  Swal.fire({
    title: "Work in Progress",
    html: "city details feature is coming soon ...",
    showConfirmButton: false,
    showCancelButton: true,
    cancelButtonText: "Close"
  });
}

async function main() {
  await initMap();
  await applyMarkers();
}

onMounted(() => {
  console.log("search number ", counter.value);
  main();
})

</script>

<template>
  <main>
    <!-- loading spinner & cities found information -->
    <div>
      <p v-if="state.foundCitiesFlag" id="foundCitiesCount">{{ state.foundCitiesCount }} cities were found</p>
      <p v-else id="loading">Loading Cities ...</p>
    </div>
    <div :id="state.mapId"></div>
  </main>
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
  font-size: large;
}

#leaflet-map {
  height: 98vh;
  width: 90%;
  overflow: hidden;
  margin: 0 auto;
  border-style: double;
}

</style>