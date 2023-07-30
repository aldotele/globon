<script setup>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer, LPolygon, LGeoJson } from "@vue-leaflet/vue-leaflet"
import { ref } from 'vue'
import { isProxy, toRaw } from 'vue';



const props = defineProps({
            iso3Codes: Array,
          })

console.log(props.iso3Codes)
console.log(toRaw(props.iso3Codes)[0])

// api of all world countries borders coordinates
const COUNTRIES_BORDERS = import.meta.env.VITE_COUNTRIES_BORDERS_GEOJSON;

let zoom = ref(3)
let center = ref([30, 15])

const polygons = ref([])

fetch(COUNTRIES_BORDERS, { method: 'GET', redirect: 'follow'})
    .then((response) => response.json())
    .then((geoJson) => geoJson.features.forEach((country) => {
        if ([props.iso3Codes.value].includes(country.properties.ISO_A3)) {
          polygons.value.push(country)
        }
    }))

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
      <l-map style="display:block" ref="map" v-model:zoom="zoom" v-model:center="center" :useGlobalLeaflet="false">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      layer-type="base"
                      name="Open Street Map">
        </l-tile-layer>
        <l-geo-json v-for="(polygon, index) in polygons" :key="index" :geojson="polygon" :style="{ color: 'red', fill: false }" />
        <!-- <l-geo-json :geojson="geojson" :style="{ color: 'red', fill: false }" /> -->
        <!-- <l-polygon v-for="(polygon, index) in polygons" :key="index" :lat-lngs="polygon" color="red" :fill="false" /> -->
        <!-- {/* <l-polygon :lat-lngs="polygon" color="red" :fill="false" /> */} -->
      </l-map>

    </main>
</template>

<style lang="scss" scoped>
html, body {
    margin: 0;
    padding: 0;
  }
  
  main {
    height: 60vh;
    width: 95vw;
    margin: 200px auto 30px auto;
  }
</style>