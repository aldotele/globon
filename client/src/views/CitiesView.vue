<script setup>
import { ref, reactive, onMounted } from 'vue'

import CityMap from '../components/CityMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    iso3: null,
    minPopulation: null,
    maxPopulation: null,
    capital: null
})

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the city ids of filtered cities
let citiesIdToCoords = [];

const countryNameToIso = ref({});
const manyItemsMsg = ref(false);

onMounted(async () => {
    // GRAPHQL query for countries
    let query = `{
        countries {
            iso3,
            iso2,
            name
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
        res.data.countries
            .forEach(country => countryNameToIso.value[country.name] = country.iso3);

    } catch (error) {
        console.log('Error fetching countries:', error);
    }
});

const afterSubmit = async () => {
    // building the composite filter
    // example: (search: "iso3=ITA&capital=primary")
    let compositeFilterList = []

    if (filters.iso3) {
        compositeFilterList.push("iso3=" + filters.iso3);
    }
    if (filters.minPopulation) {
        compositeFilterList.push("population>" + filters.minPopulation);
    }
    if (filters.maxPopulation) {
        compositeFilterList.push("population<" + filters.maxPopulation);
    }
    if (filters.capital) {
        compositeFilterList.push("capital=primary");
    }

    const compositeFilter = compositeFilterList.join("&");

    // GRAPHQL query for cities
    let query = `{
        cities(search: "${compositeFilter}") {
            iso3,
            city,
            lat,
            lng,
            smId
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

        if ("errors" in res) {
            isSubmitted.value = false;
            manyItemsMsg.value = true;
        } else {
            manyItemsMsg.value = false;
            citiesIdToCoords = await extractCitiesIdToCoords(res.data.cities);
            isSubmitted.value = true;
            //console.log("submitted !")
            searchCount.value++;
        }
    } catch (error) {
        console.log(error);
    }
}

async function extractCitiesIdToCoords(data) {
    let res = []
    data.forEach((city) => {
        let city_id = city.smId;
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
        <form @submit.prevent="onSubmit">
            <div id="form-input-div">

                <!-- COUNTRY -->
                <div class="filter-input-div">
                    <label for="country">Country &nbsp;&nbsp;</label>
                    <select id="country" name="country" v-model="filters.iso3">
                        <option value="">- - - select - - -</option>
                        <option :key="countryNameToIso[countryName]" :value="countryNameToIso[countryName]" v-for="countryName in Object.keys(countryNameToIso).sort()">{{ countryName }}</option>
                    </select>
                </div>

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

                <!-- CAPITAL -->
                <div class="filter-input-div">
                    <label for="capital"> only capitals</label><br>
                    <input type="checkbox" id="capital-flag" name="capital" value="capital" v-model="filters.capital">
                </div>

            </div>

            <div id="submit-section" class="button-block">
                <button @click="afterSubmit" class="submit-button" type="submit">Find Cities</button>
            </div>

        </form>

    </div>

    <p id="many-msg" v-if="manyItemsMsg">Too many cities to display on map. Please narrow down your search.</p>

    <CityMap v-if="isSubmitted" :citiesIdToCoords="citiesIdToCoords" :searchCount="searchCount" :filters="filters" />

</template>

<style lang="scss" scoped>
* {
  font-family: 'Roboto Mono';
}

.input-wrapper {
    display: flex;
    justify-content: center;
    padding-top: 30px;
}

#country {
    width: 150px;
    font-size: medium;
}

#capital-flag {
    width: 100px;
    height: 15px;
}

form {
    text-align: center;
    margin-top: 10px;
}

#form-input-div {
    width: 700px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

.filter-input-div {
    margin: 10px 5px;
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

#many-msg {
    text-align: center;
    text-decoration: underline;
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