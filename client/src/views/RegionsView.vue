<script setup>
import { ref, reactive, onMounted } from 'vue'

import RegionMap from '../components/RegionMap.vue';

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

let filters = reactive({
    countryName: null,
    iso2: null,
    iso3: null,
    region: null
})

let searchCount = ref(0);
let isSubmitted = ref(false);

// will hold the regions
let regions = ref(null);

const countryNameToIso2 = ref({});

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
            .forEach(country => countryNameToIso2.value[country.name] = country.iso2);

    } catch (error) {
        console.log('Error fetching countries:', error);
    }
});

const onChange = async () => {
    filters.region = null;
    filters.iso2 = countryNameToIso2.value[filters.countryName];
    // here we have the value of the iso2
    // iso2 can be used to find all regions of a country
    // then a separate request for each region will retrieve the geoJson
    try {
        // Make an API request to fetch regions
        const response = await fetch(SERVER_ADDRESS+"/api/regions/"+filters.iso2, {method: 'GET', redirect: 'follow'});
        // update the regions ref which will activate the Region dropdown
        regions.value = await response.json();
        //console.log(regions)
    } catch (error) {
        console.error('Error fetching countries:', error);
    }

}

const afterSubmit = async () => {
    // here we have the value of the iso3
    // iso3 can be used to find all regions of a country
    // then a separate request for each region will retrieve the geoJson
    try {
        // update submission flag to open RegionMap
        isSubmitted.value = true;
        //console.log("submitted !")
        searchCount.value++;

    } catch (error) {
        console.error('Error fetching countries:', error);
    }

}
</script>

<template>
    <div class="input-wrapper">
        <form @submit.prevent="onSubmit">
            <div id="form-input-div">

                <!-- COUNTRY -->
                <div class="filter-input-div">
                    <label for="country">Country &nbsp;&nbsp;</label>
                    <select @change="onChange" id="country" name="country" v-model="filters.countryName">
                        <option value="">- - - select - - -</option>
                        <option :key="countryName" :value="countryName" v-for="countryName in Object.keys(countryNameToIso2).sort()">{{ countryName }}</option>
                    </select>
                </div>

                <!-- REGION -->
                <div v-if="regions" class="filter-input-div">
                    <label for="region">Region &nbsp;&nbsp;</label>
                    <select id="region" name="region" v-model="filters.region">
                        <option value="">- - - select - - -</option>
                        <option :key="region" :value="region" v-for="region in regions">{{ region }}</option>
                    </select>
                </div>

            </div>

            <div id="submit-section" class="button-block">
                <button :disabled="!filters.iso2" @click="afterSubmit" class="submit-button" type="submit">Find Regions</button>
            </div>

        </form>

    </div>

    <RegionMap v-if="isSubmitted" :searchCount="searchCount" :filters="filters" />

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

select {
    width: 150px;
    font-size: medium;
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

.submit-button:disabled {
    cursor: default;
    font-weight: 500;
    color: rgb(150, 150, 150);
    background-color: rgb(216, 215, 215);
    border-color: rgb(150, 150, 150);
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