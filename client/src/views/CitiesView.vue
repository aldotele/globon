<script setup>
import { ref, onMounted } from 'vue'
import { defineEmits, reactive, toRefs } from "vue"

import GlobonCityMap from '../components/GlobonCityMap.vue';


const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    minPopulation: null,
    maxPopulation: null,
    iso3: null,
})

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the city ids of filtered cities
let citiesCoords = [];

const countryNameToIso = ref({});
const manyItemsMsg = ref(false);

onMounted(async () => {
  try {
    // Make an API request to fetch countries and populate the countries ref
    const response = await fetch(SERVER_ADDRESS+"/api/countries", {method: 'GET', redirect: 'follow'});
    const data = await response.json();

    data.forEach((country) => {
        countryNameToIso.value[country.name] = country.iso_code;
    })
    countryNameToIso.value
  } catch (error) {
    console.error('Error fetching countries:', error);
  }
});


const afterSubmit = async () => {
    console.log(filters);
    let uri = SERVER_ADDRESS+"/api/cities?";
    uri = filters.iso3 ? uri + `iso3=${filters.iso3}&` : uri;
    uri = filters.minPopulation ? uri + `minPopulation=${filters.minPopulation}&` : uri;
    uri = filters.maxPopulation ? uri + `maxPopulation=${filters.maxPopulation}&` : uri;

    const response = await fetch(uri, {method: 'GET', redirect: 'follow'});
    const data = await response.json();

    if (response.status == 403) {
        isSubmitted.value = false;
        manyItemsMsg.value = true;
    } 

    if (response.status == 200) {
        manyItemsMsg.value = false;
        citiesCoords = await extractCityCoords(data);
        isSubmitted.value = true;
        console.log("submitted !")
        searchCount.value++;
    }
}

async function extractCityCoords(data) {
    let coords = []
    data.forEach((city) => {
        coords.push([city.lat, city.lng])
    })
    return coords;
}

</script>

<template>
    <div class="input-wrapper">
        <!-- COUNTRY form -->
        <form>
            <label for="country">Country: &nbsp;&nbsp;</label>
            <select id="country" name="country" v-model="filters.iso3">
                <option value="">- - - select - - -</option>
                <option :key="countryNameToIso[countryName]" :value="countryNameToIso[countryName]" v-for="countryName in Object.keys(countryNameToIso).sort()">{{ countryName }}</option>
                <option :key="iso" :value="iso" v-for="(iso, countryName) in countryNameToIso">{{ countryName }}</option>
            </select>
        </form>

        <!-- POPULATION form -->
        <form>
            <p>
            <label for="minPopulation">Min Population: &nbsp;&nbsp; </label>
            <input type="text" id="minPopulation" name="minPopulation" v-model="filters.minPopulation">
            </p>
        
            <p>
            <label for="maxPopulation">Max Population: &nbsp;&nbsp; </label>
            <input type="text" id="maxPopulation" name="maxPopulation" v-model="filters.maxPopulation">
            </p>
        </form>

        <div>
            <button @click="afterSubmit" class="submit-button" type="submit">Search Cities</button>
        </div>
    </div>

    <p id="many-msg" v-if="manyItemsMsg">Too many cities to display on map. Please narrow down your search.</p>

    <GlobonCityMap v-if="isSubmitted" :citiesCoords="citiesCoords" :searchCount="searchCount" />

</template>

<style lang="scss" scoped>
* {
font-family: 'Open Sans', sans-serif;
}
.input-wrapper {
    display: flex;
    justify-content: space-evenly;
    width: 80%;
    align-items: center;   
}

#search {
    width: 180px;
}

#search-by {
    margin-top: 30px;
}

#country {
    width: 100px;
}

form {
    margin-top: 30px;
}


.submit-button {
  cursor: pointer;
  font-weight: 700;
  border: 1px solid black;
  color: black;
  padding: 6px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin-top: 20px;
}

.submit-button:hover {
    color: white;
    background-color: #42e048;
}

#many-msg {
    text-align: center;
    text-decoration: underline;
}

</style>