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
const countryChange = computed(() => props.filters.countryName)

// clear map whenever either a new country or region is selected without submitting a new search
watch(countryChange, async () => {
  await clearBorders();
  state.foundRegionFlag = false;
})
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
    layers: [],
  },
  geoJsonData: null,
  mapInstance: null,
  borderGroup: null,
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

  state.mapInstance = leafletMap;
}

async function clearBorders() {
  state.mapInstance.removeLayer(state.borderGroup);
}

// fetch data
async function drawRegion() {
  // loading spinner activated
  state.loadingRegion = true;
  let noRegionFilter = "";
  let REGIONS_API = `https://nominatim.openstreetmap.org/search.php?country=${props.filters.countryName}&state=${props.filters.region?props.filters.region:noRegionFilter}&polygon_geojson=1&format=jsonv2`;
  let response = await fetch(REGIONS_API, { method: 'GET', redirect: 'follow'});
  let responseBody = await response.json()
  const fields = ["geojson", "lat", "lon"];
  if (responseBody && responseBody.length == 1 && fields.every((field) => field in responseBody[0])) {
    let regionData = responseBody[0];
    // update the center of the map to the region
    let lat = regionData.lat;
    let lon = regionData.lon;
    state.mapInstance.setView(new L.LatLng(lat, lon), 5);
    // found region flag
    state.foundRegionFlag = true;
    let geojson = regionData.geojson;
    const border = L.geoJSON(geojson)
      .setStyle(mapStyle)
      .on('click', function() {
        retrieveCapital(props.filters.region);
      });
    state.borderGroup = L.layerGroup([border]).addTo(state.mapInstance);
    // deactivate spinner after region was found   
    state.loadingRegion = false;
  } else {
    // reset to world center
    state.mapInstance.setView(state.mapOptions.center, 3);
    // deactivate spinner when nothing was found
    state.loadingRegion = false;
  }
}

async function retrieveCapital(region) {
  let query;
  // if region is not chosen then the country capital is retrieved
  if (region) {
    query = `{
      cities(search: "admin_name=${region} & capital = admin|primary") {
        city
      }
    }`;
  } else {
    query = `{
      cities(search: "iso2=${props.filters.iso2} & capital = primary") {
        city
      }
    }`;   
  }

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
      triggerCapitalAlert(region ? region : props.filters.countryName, res.data.cities[0].city)
    }
  } catch (error) {
      console.log(error);
  }
}

async function triggerCapitalAlert(region, city) {

  let builtHtml = `
    <h3 style='font-weight:500'>
    <b>capital</b>: ${city}</h3>
  `;
  
  // triggering alert with country info
  Swal.fire({
    title: region,
    html: builtHtml,
    showConfirmButton: false,
    showCancelButton: true,
    cancelButtonText: "Close"
  });
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