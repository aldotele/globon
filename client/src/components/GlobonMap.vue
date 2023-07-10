<script setup>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet"
import { ref } from 'vue'

let zoom = ref(3)
let center = ref([30, 15])
</script>

<template>
    <main>
      <l-map ref="map" v-model:zoom="zoom" v-model:center="center" :useGlobalLeaflet="false">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      layer-type="base"
                      name="Open Street Map"></l-tile-layer>
      </l-map>
    </main>
</template>

<style lang="scss" scoped>
html, body {
    margin: 0;
    padding: 0;
  }
  
  main {
    height: 100vh;
    width: 100vw;
  }
</style>