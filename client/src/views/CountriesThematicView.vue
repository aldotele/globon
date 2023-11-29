<script setup>
import { normalizeClass, reactive, ref } from "vue"

import CountryThematicMap from '../components/CountryThematicMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the country codes of filtered countries
let isoToNormalized = {}

const afterSubmit = async () => {
    const api = "/api/countries/society?fields=country_id,population";

    const response = await fetch(SERVER_ADDRESS+api, {method: 'GET', redirect: 'follow'});
    const data = await response.json();
    console.log(data)

    // finding max and min value to normalize data
    const maxPopulationValue = Math.max(...data.map(o => o.population), 0);
    const minPopulationValue = Math.min(...data.map(o => o.population), 0);

    let country_id_key = "country_id";
    isoToNormalized = await normalize(data, country_id_key, minPopulationValue, maxPopulationValue);

    isSubmitted.value = true;
    console.log("submitted !")
    searchCount.value++;
}

async function normalize(data, id, minValue, maxValue) {
    let res = {}
    data.forEach((country) => {
        let normalizedValue = (country.population - minValue) / (maxValue - minValue)
        res[country[id]] = normalizedValue;
    })
    return res;
}

</script>

<template>
    <div class="input-wrapper">

        <!-- FAKE form -->
        <form @submit.prevent="onSubmit">            
            <div class="button-block">
                <button @click="afterSubmit" class="submit-button" type="submit">Submit</button>
            </div>
        </form>
    </div>
    <CountryThematicMap v-if="isSubmitted" :isoToNormalized="isoToNormalized" :searchCount="searchCount" />
</template>

<style lang="scss" scoped>

* {
font-family: 'Open Sans', sans-serif;
}
.input-wrapper {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

#search {
    width: 180px;
}

#search-by {
    margin-top: 30px;
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

@media screen and (max-width: 600px) {
    .input-wrapper {
        flex-direction: column;
    }

    .button-block {
        text-align: center;
        margin-top: 20px;
    }
}
</style>