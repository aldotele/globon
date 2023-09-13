<script setup>
import router from "@/router";
import Swal from 'sweetalert2';


// navigate to the selected section
const discoverCountries = () => {
    router.push("/countries");
}

const discoverCities = () => {
    Swal.fire({
    title: "Work in progress",
    html: "the cities section is coming soon ...",
    showConfirmButton: false,
    showCancelButton: true,
    cancelButtonText: "Close"
    });
    
    //router.push("/cities");
}

</script>

<template>
  <main>
    <h1>Discover&nbsp:</h1>
        <div class="discover-wrapper">
            <button class="discover-button" @click="discoverCountries()">COUNTRIES</button>
            <button class="discover-button" @click="discoverCities()">CITIES</button>
        </div>
  </main>
</template>

<style lang="scss" scoped>
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
    width: 250px;
    height: 80px;
    margin: 0 10px;
    cursor: pointer;
    font-weight: 500;
    border: 0.5px solid black;
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
  }

}
</style>
