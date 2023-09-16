<script setup>
import { ref, reactive, onMounted } from 'vue'

import CityMap from '../components/CityMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    iso3: null,
    minPopulation: null,
    maxPopulation: null,
})

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the city ids of filtered cities
let citiesIdToCoords = [];

const countryNameToIso = ref({});
const manyItemsMsg = ref(false);

onMounted(async () => {
  try {
    // Make an API request to fetch countries and populate the coutryNameToIso ref
    const response = await fetch(SERVER_ADDRESS+"/api/countries", {method: 'GET', redirect: 'follow'});
    const data = await response.json();

    // countryNameToIso object is used to populate the dropdown country filter
    data.forEach((country) => {
        countryNameToIso.value[country.name] = country.iso_code;
    })
  } catch (error) {
    console.error('Error fetching countries:', error);
  }
});

const afterSubmit = async () => {
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
        citiesIdToCoords = await extractCitiesIdToCoords(data);
        isSubmitted.value = true;
        //console.log("submitted !")
        searchCount.value++;
    }
}

async function extractCitiesIdToCoords(data) {
    let res = []
    data.forEach((city) => {
        let city_id = city.sm_id;
        let city_coords = [city.lat, city.lng];
        let cityIdToCoords = {};
        cityIdToCoords[city_id] = city_coords
        res.push(cityIdToCoords);
    })
    return res;
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

    <CityMap v-if="isSubmitted" :citiesIdToCoords="citiesIdToCoords" :searchCount="searchCount" :filters="filters" />

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