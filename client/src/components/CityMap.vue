<script setup>
import { reactive, onMounted, watch, computed } from 'vue'
import L from 'leaflet';
import Swal from 'sweetalert2';


const props = defineProps({
  citiesIdToCoords: Array,
  searchCount: Number,
  filters: Object
})

const counter = computed(() => props.searchCount);

// a new search will increment the counter, therefore previous markers will be removed first
watch(counter, async () => {
  await clearMarkers();
  // clear also the found cities description
  state.foundCitiesFlag = false;
  // fetching data again
  applyMarkers();
}, {
  // deep property set to true allows to track nested properties changes also
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
  console.log("search number ", counter.value);
  state.foundCitiesCount = props.citiesIdToCoords.length;
  // before applying markers, create a marker group for the current search
  state.markerGroup = L.layerGroup().addTo(state.mapInstance)
  // center map on the country if a country filter is present
  if (state.foundCitiesCount > 0 && props.filters.iso3) {
    const firstCoords = Object.values(props.citiesIdToCoords[0])[0];
    state.mapInstance.setView(new L.LatLng(firstCoords[0], firstCoords[1]), 5);
  } else {
    // reset to world center
    state.mapInstance.setView(state.mapOptions.center, 3);
  }
  props.citiesIdToCoords.forEach((cityIdToCoords) => {
    // creating a new marker with lat, lng and add it to the group
    // note that cityIdToCoords is an object with key->sm_id and value->[lat, lng]
    const marker = L.marker(Object.values(cityIdToCoords)[0]);
    marker.addTo(state.markerGroup)
    .on('click', function() {
      showCityDetails(Object.keys(cityIdToCoords)[0]);
    });
  })

  state.foundCitiesFlag = true;
}

async function showCityDetails(city_id) {
  const response = await fetch(import.meta.env.VITE_SERVER_ADDRESS + "/api/cities?smId=" + city_id);
  const body = await response.json();
  if (body.length > 0) {
    let city = body[0];
    // center the map on the city
    let newZoomLevel = state.mapInstance.getZoom() > 6 ? state.mapInstance.getZoom() : 6;
    state.mapInstance.setView(new L.LatLng(city.lat, city.lng), newZoomLevel);

    triggerCountryAlert(city);
  }
}

async function triggerCountryAlert(data) {
  // notes will be added if city is either a country/region/county capital
  let notes = data.capital == "primary" ? "capital city" : 
  data.capital == "admin" ? "region capital" 
  : data.capital == "minor" ? "county capital" 
  : "";

  let builtHtml = `
    <h3 style='font-weight:500'>
    <b>population</b>: ${data.population ? data.population.toLocaleString() : "n/a"}<br><br>
    <b>country</b>: ${data.country}<br><br>
    <b>region</b>: ${data.admin_name}<br><br>
  `;
  
  if (notes) {
    builtHtml += `<b>notes</b>: ${notes}<br><br>`;
  }
  builtHtml += "</h3>";
  
  // triggering alert with country info
  Swal.fire({
    title: data.city,
    html: builtHtml,
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