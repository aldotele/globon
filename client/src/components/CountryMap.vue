<script setup>

import { reactive, onMounted, watch, computed } from 'vue'
import L from 'leaflet';
import Swal from 'sweetalert2';

const props = defineProps({
  iso3Codes: Array,
  searchCount: Number
})

const counter = computed(() => props.searchCount);

// a new search will increment the counter, therefore previous borders will be removed first
watch(counter, async () => {
  // clear found countries flag
  state.foundCountriesFlag = false;
  await clearBorders();
  // fetching data again
  applyBorders();
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
  geoJsonData: null,
  mapInstance: null,
  borderGroup: null,
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

  state.mapInstance = leafletMap;
}

async function clearBorders() {
  if (state.borderGroup) {
    state.mapInstance.removeLayer(state.borderGroup);
  }
}

// fetch data
async function fetchAllGeoJsonBorders() {
  // api of all world countries borders coordinates
  const COUNTRIES_BORDERS = import.meta.env.VITE_COUNTRIES_BORDERS_GEOJSON;
  const response = await fetch(COUNTRIES_BORDERS, { method: 'GET', redirect: 'follow'});
  state.geoJsonData = await response.json();
}

async function applyBorders() {
  let borders = [];
  state.geoJsonData.features.forEach((geoJsonCountry) => {
    if (props.iso3Codes.includes(geoJsonCountry.id)) {
      const border = L.geoJSON(geoJsonCountry)
        .setStyle(mapStyle)
        .on('click', showCountryDetails);
      borders.push(border);
    }
  })
  // creade group of borders with all filtered borders inside it
  state.borderGroup = L.layerGroup(borders).addTo(state.mapInstance);
  state.foundCountriesCount = props.iso3Codes.length;
  state.foundCountriesFlag = true;
}

async function showCountryDetails(e) {
  let isoCode = e.layer.feature.properties.ISO_A3;
  let isoFilter = "(search: \"iso3 = " + isoCode + "\")";
  let query = `{
    countries${isoFilter} {
        iso3,
        name,
        capital,
        society {
            population
        }
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
    if (res.data.countries.length > 0) {
      triggerCountryAlert(res.data.countries[0])
    }
  } catch (error) {
      console.log(error);
  }
}


async function triggerCountryAlert(data) {
  // triggering alert with country info
  let capital = data.capital ? data.capital.replace("[", "").replace("]", "") : "-";
  let population = data.society.population ? data.society.population.toLocaleString() : "-";
  Swal.fire({
    title: `<h3 style='font-weight:500;font-family:Roboto Mono'>${data.name}</h3>`,
    html: "<h3 style='font-weight:500;font-family:Roboto Mono'>" 
    + `<p style='font-weight:300'><b>population</b>: ${population}<br><br>` 
    + `<b>capital city</b>: ${capital}<br><br>`
    //+ "<b>currencies</b>: " + data.currencies.join(", ") + "<br><br>"
    //+ "<b>spoken languages</b>: " + data.languages.join(", ")
    + "</p></h3>",
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