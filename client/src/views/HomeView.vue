<script setup>
import router from "@/router";

const welcomeMessage = "Welcome To World Proxy";
let isReady = false;

// contacting the server
const launch = () => {
  fetch(import.meta.env.VITE_SERVER_ADDRESS, { method: 'GET', redirect: 'follow'})
    .then(response => { 
      if (response.status == 200) {
        isReady = true;
        console.log("Ready: ", isReady);
        // when server is up and running, navigate to the countries section
        router.push("/countries");
      }
    })
    .catch(error => {
      console.log(error);
        // handle the error
    });
  console.log("executed");
}

</script>

<template>
  <main>
      <h1>The World at your fingertips</h1>
      <!-- <router-link class="start-btn" :to="{ path: '/countries' }"><button class="start-btn">Start Discovering</button></router-link> -->
      <button class="start-btn" @click="launch()">Start Discovering</button>
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

  .start-btn {
    height: 45px;
    width: 250px;
    margin: 0 auto;
  }
}
</style>
