<script setup>
import { reactive, ref } from "vue"

import CountryMap from '../components/CountryMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
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
    // building the composite filter
    // example: (search: "society.population>1000&income_level=UMC")
    let compositeFilter = ""

    if (filters.minPopulation) {
        compositeFilter += "society.population>" + filters.minPopulation + "&";
    }
    if (filters.maxPopulation) {
        compositeFilter += "society.population<" + filters.maxPopulation + "&";
    }
    if (filters.incomeLevel) {
        compositeFilter += "income_level=" + filters.incomeLevel;
    }

    // GRAPHQL query for countries
    let query = `{
        countries(search: "${compositeFilter}") {
            iso3,
            society {
                population
            }
        }
    }`;
    
    try {
        let res = await fetch(SERVER_ADDRESS+'/graphql', {
            method: 'POST',
            headers: {
            'content-type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });
        res = await res.json();
        iso3Codes = res.data.countries.map(element => element.iso3);
        isSubmitted.value = true;
        searchCount.value++;

    } catch (error) {
        console.log(error);
    }

}

</script>


<template>
    <div class="input-wrapper">

        <form @submit.prevent="onSubmit">

            <div id="form-input-div">
        
                <!-- MIN POPULATION -->
                <div class="filter-input-div">
                    <label for="minPopulation">Min Population &nbsp;&nbsp; </label>
                    <input type="text" id="minPopulation" name="minPopulation" v-model="filters.minPopulation">
                </div>

                <!-- MAX POPULATION -->
                <div class="filter-input-div">
                    <label for="maxPopulation">Max Population &nbsp;&nbsp; </label>
                    <input type="text" id="maxPopulation" name="maxPopulation" v-model="filters.maxPopulation">
                </div>

                <!-- INCOME -->
                <div class="filter-input-div">
                    <label for="incomeLevel">Income Level&nbsp;&nbsp;</label>
                    <select id="incomeLevel" name="incomeLevel" v-model="filters.incomeLevel">
                        <option value="">- - - select - - -</option>
                        <option value="HIC">HIGH</option>
                        <option value="UMC">UPPER MIDDLE</option>
                        <option value="LMC">LOWER MIDDLE</option>
                        <option value="LIC">LOW</option>
                    </select>
                </div>

            </div>

            <div class="button-block">
                <button @click="afterSubmit" class="submit-button" type="submit">Find Countries</button>
            </div>

        </form>
    </div>

    <CountryMap v-if="isSubmitted" :iso3Codes="iso3Codes" :searchCount="searchCount" />
</template>


<style lang="scss" scoped>

* {
font-family: 'Open Sans', sans-serif;
}
.input-wrapper {
    display: flex;
    justify-content: center;
    padding-top: 30px;
}

form {
    text-align: center;
    margin-top: 10px;
}

#form-input-div {
    width: 500px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

.filter-input-div {
    margin: 5px 5px;
}

#incomeLevel {
    width: 150px;
    font-size: medium;
}

.button-block {
    text-align: center;
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
}

.submit-button:hover {
    color: white;
    background-color: #42e048;
}

@media screen and (max-width: 600px) {
    .input-wrapper {
        flex-direction: column;
    }

    #form-input-div {
        width: 100%;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
    }

    .button-block {
        text-align: center;
        margin-top: 20px;
    }
}
</style>