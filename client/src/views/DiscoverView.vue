<script setup>
import router from "@/router";

const discover = (value) => {
  router.push("/" + value);
}

</script>

<template>
  <main>
    <h1>Discover&nbsp:</h1>
        <div class="discover-wrapper">
            <button class="discover-button" @click="discover('countries')">COUNTRIES</button>
            <button class="discover-button" @click="discover('cities')">CITIES</button>
            <button class="discover-button" @click="discover('regions')">REGIONS</button>
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
