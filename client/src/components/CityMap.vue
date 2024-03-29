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
  if (state.markerGroup) {
    state.mapInstance.removeLayer(state.markerGroup);
  }
}

async function applyMarkers() {
  //console.log("search number ", counter.value);
  state.foundCitiesCount = props.citiesIdToCoords.length;
  let markers = []
  // center map on the country if a country filter is present
  if (state.foundCitiesCount > 0 && props.filters.iso3) {
    const firstCoords = Object.values(props.citiesIdToCoords[0])[0];
    state.mapInstance.setView(new L.LatLng(firstCoords[0], firstCoords[1]), 5);
  } else {
    // reset to world center
    state.mapInstance.setView(state.mapOptions.center, 3);
  }
  props.citiesIdToCoords.forEach((cityIdToCoords) => {
    // creating a new marker with lat, lng
    // note that cityIdToCoords is an object with key->sm_id and value->[lat, lng]
    const marker = L.marker(Object.values(cityIdToCoords)[0])
      .on('click', function() {
        showCityDetails(Object.keys(cityIdToCoords)[0]);
      });
    markers.push(marker);
  })
  // add all markers at once to the same layer group
  state.markerGroup = L.layerGroup(markers).addTo(state.mapInstance);
  state.foundCitiesFlag = true;
}

async function showCityDetails(city_id) {
  let query = `{
    cities(search: "sm_id=${city_id}") {
        iso3,
        city,
        capital,
        country,
        adminName,
        population,
        lat,
        lng,
        smId
    }
  }`;

  try {
    let res = await fetch(import.meta.env.VITE_SERVER_ADDRESS+'/graphql', {
      method: 'POST',
      headers: {
      'content-type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    res = await res.json();
    if (res.data.cities.length > 0) {
      triggerCityAlert(res.data.cities[0])
    }
  } catch (error) {
      console.log(error);
  }
}

async function triggerCityAlert(data) {
  // notes will be added if city is either a country/region/county capital
  let notes = data.capital == "primary" ? "capital city" : 
  data.capital == "admin" ? "region capital" 
  : data.capital == "minor" ? "county capital" 
  : "";

  let builtHtml = `
    <h3 style='font-weight:500;font-family:Roboto Mono'>
    <p style='font-weight:300'><b>population</b>: ${data.population ? data.population.toLocaleString() : "n/a"}<br><br>
    <b>country</b>: ${data.country}<br><br>
  `;

  if (data.adminName) {
    builtHtml += `<b>region</b>: ${data.adminName}<br><br>`;
  }
  
  if (notes) {
    builtHtml += `<b>notes</b>: ${notes}<br><br>`;
  }
  builtHtml += "</p></h3>";
  
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

* {
  font-family: 'Roboto Mono';
}
  
main {
  margin: 75px auto 30px auto;
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

@media screen and (max-width: 600px) {
  main {
    margin-bottom: 50px;
  }

  #leaflet-map {
    height: 85vh;
    width: 85%;
  }
}

</style>