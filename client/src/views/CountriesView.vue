<script setup>
import { ref } from 'vue'
import { defineEmits, reactive, toRefs } from "vue"


import GlobonMap from '../components/GlobonMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    type: null,
    minPopulation: null,
    maxPopulation: null,
    incomeLevel: null,
    isSubmitted: false,
    iso3Codes: []
})

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the country codes of filtered countries
let iso3Codes = [];

const afterSubmit = async () => {
    let uri = SERVER_ADDRESS+"/api/countries?";

    switch (filters.type) {
    case 'population':
        uri = filters.minPopulation ? uri + `minPopulation=${filters.minPopulation}&` : uri;
        uri = filters.maxPopulation ? uri + `maxPopulation=${filters.maxPopulation}&` : uri;
        break;
    case 'incomeLevel':
        uri = filters.incomeLevel ? uri + `incomeLevel=${filters.incomeLevel}&` : uri;
        break;
    default:
        console.log(`No filters applied.`);
    }

    const response = await fetch(uri, {method: 'GET', redirect: 'follow'});
    const data = await response.json();
    iso3Codes = await extractCountryCodes(data);

    isSubmitted.value = true;
    console.log("submitted !")
    searchCount.value++;
}

async function extractCountryCodes(data) {
    let codes = []
    data.forEach((country) => {
        codes.push(country.iso_code);
    })
    return codes;
}


</script>

<template>
    <div class="input-wrapper">
        <div id=search-by>

            <!-- search by -->
            <label style="font-size: 25px" for="search">Search countries by:<br> &nbsp;&nbsp; </label>

            <select name="search" id="search" v-model="filters.type">
                <option value="">- - - select - - -</option>
                <option value="population">Population</option>
                <option value="incomeLevel">Income Level</option>
            </select>
        </div>

        <!-- POPULATION form -->
        <form v-if="filters.type=='population'" @submit.prevent="onSubmit">
        
            <p>
            <label for="minPopulation">Min Population: &nbsp;&nbsp; </label>
            <input type="text" id="minPopulation" name="minPopulation" v-model="filters.minPopulation">
            </p>
        
            <p>
            <label for="maxPopulation">Max Population: &nbsp;&nbsp; </label>
            <input type="text" id="maxPopulation" name="maxPopulation" v-model="filters.maxPopulation">
            </p>
            <p>
            <!--<button class="submit-button" type="submit" [disabled]="locate.value == '' ">Submit</button>-->
            <button @click="afterSubmit" class="submit-button" type="submit">Submit</button>
            </p>
    
        </form>

        <!-- INCOME form -->
        <form v-if="filters.type=='incomeLevel'" @submit.prevent="onSubmit">
            <label for="incomeLevel">Income Level&nbsp;&nbsp;</label>
            <select id="incomeLevel" name="incomeLevel" v-model="filters.incomeLevel">
                <option value="">- - - select - - -</option>
                <option value="HIC">HIGH</option>
                <option value="UMC">UPPER MIDDLE</option>
                <option value="LMC">LOWER MIDDLE</option>
                <option value="LIC">LOW</option>
            </select>
            
            <p>
                <button @click="afterSubmit" class="submit-button" type="submit">Submit</button>
            </p>
        </form>
    </div>
    <GlobonMap v-if="isSubmitted" :iso3Codes="iso3Codes" :searchCount="searchCount" />
</template>

<style lang="scss" scoped>
.input-wrapper {
    display: flex;
    justify-content: space-evenly;
    align-items: center;   
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

</style>