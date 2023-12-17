<script setup>
import router from "@/router";
import { onMounted, ref, reactive} from 'vue'

const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

//let flags = reactive({"countries": false, "cities": true, "regions": true});
let isLoading = ref(true)
let flags = reactive({
  "countries": false,
  "cities": false,
  "regions": false
})

const discover = (value) => {
  router.push("/" + value);
}

onMounted(async () => {
  try {
    // checking if data are present per section. Using iso3 ITA
    const countryResponse = await fetch(SERVER_ADDRESS+"/api/countries?fields=iso2&iso3=ITA", {method: 'GET', redirect: 'follow'});
    const cityResponse = await fetch(SERVER_ADDRESS+"/api/cities?capital=true&iso3=ITA", {method: 'GET', redirect: 'follow'});
    
    if (countryResponse) {
      const countryBody = await countryResponse.json();
      if (countryBody.length > 0) {
        flags.countries = true;
      }
    }
    if (cityResponse) {
      const cityBody = await cityResponse.json();
      if (cityBody.length > 0) {
        flags.cities = true;
        flags.regions = true;
      }
    }
    // opens the sections container
    isLoading.value = false;
  } catch (error) {
        console.error('Error fetching data:', error);
  }
})

</script>

<template>
  <main>
    <h1>Discover&nbsp</h1>
        <div v-if="!isLoading" class="discover-wrapper">
            <button v-if="flags.countries" class="discover-button" @click="discover('countries')">Countries</button>
            <button v-if="flags.cities" class="discover-button" @click="discover('cities')">Cities</button>
            <button v-if="flags.regions" class="discover-button" @click="discover('regions')">Regions</button>
        </div>
  </main>
</template>

<style lang="scss" scoped>
* {
  font-family: 'Roboto Mono';
}

main {
  display: flex;
  flex-direction: column;
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 16px;

  h1 {
    margin-bottom: 16px;
    text-align: center;
  }

  .discover-wrapper {
    display: flex;
    justify-content: space-around;
    align-content: space-around;
  }

  p {
    text-align: center;
  }

  .discover-button {
    min-width: 200px;
    height: 80px;
    margin: 0 10px;
    cursor: pointer;
    font-weight: bold;
    border: 0.5px dotted rgb(169, 165, 165);
    color: black;
    padding: 6px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 18px;
    margin-top: 20px;
  }

  .discover-button:hover {
    color: white;
    background-color: #42e048;
    border: 1px solid black;
  }

  @media screen and (max-width: 600px) {
    .discover-wrapper {
        flex-direction: column;
    }
}
}
</style>
