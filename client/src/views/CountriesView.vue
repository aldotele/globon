<script setup>
import { ref } from 'vue'
import { defineEmits, reactive, toRefs } from "vue"


import GlobonMap from '../components/GlobonMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    minPopulation: null,
    maxPopulation: null,
    isSubmitted: false,
    iso3Codes: []
})

let isSubmitted = ref(false);

// will hold the country codes of filtered countries
const iso3Codes = ref([]);

const afterSubmit = () => {
    fetch(SERVER_ADDRESS+"/api/countries?minPopulation="+filters.minPopulation+"&maxPopulation="+filters.maxPopulation,
     { method: 'GET', redirect: 'follow'})
    .then((response) => response.json())
    .then((json) => json.forEach((country) => {
        iso3Codes.value.push(country.iso_code)
    }))
    console.log("submitted !")
    isSubmitted.value = true;
}

</script>

<template>
    <div class="input-wrapper">
        <div id=select-by>

            <!-- search by -->
            <label style="font-size: 25px" for="search">Search countries by:<br> &nbsp;&nbsp; </label>

            <select name="search" id="search">
                <option value="">- - - select - - -</option>
                <option value="population">Population</option>
                <option value="incomeLevel">Income Level</option>
            </select>
        </div>

        <!-- POPULATION form -->
        <form @submit.prevent="onSubmit">
        
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
    </div>
    <GlobonMap v-if="isSubmitted" :iso3Codes="iso3Codes" />
</template>

<style lang="scss" scoped>
.input-wrapper {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    
}

</style>