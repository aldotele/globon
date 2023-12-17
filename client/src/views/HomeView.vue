<script setup>
import router from "@/router";
import { reactive } from "vue"

const WELCOME_MESSAGE = "Welcome To World Proxy";
const SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

const state = reactive({
  isReady: false,
  isLaunched: false
})

// contacting the server
const launch = () => {
  // user has launched the application
  state.isLaunched = true;
  fetch(SERVER_ADDRESS, { method: 'GET', redirect: 'follow'})
    .then((response) => response.text())
    .then((text) => {
      if (text.includes(WELCOME_MESSAGE)) {
        // server is ready
        state.isReady = true;
        // when server is up and running, navigate to the countries section
        router.push("/discover");
      }
    })
    .catch(error => {
      console.log(error);
        // handle the error
    });
}

</script>

<template>
  <main>
      <h1>The World at your fingertips</h1>
      <!-- <router-link class="start-btn" :to="{ path: '/countries' }"><button class="start-btn">Start Discovering</button></router-link> -->
      <button class="start-button" @click="launch()">Start Discovering</button>
      <div v-if="state.isLaunched && !state.isReady">
        <p>Please Wait . . .</p>
        <div class="loader"></div>
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
  width: 100%;
  margin: 0 auto;
  padding: 40px 16px;

  h1 {
    margin-bottom: 16px;
    text-align: center;
  }

  p {
    text-align: center;
  }

  .start-button {
    height: 45px;
    width: 250px;
    margin: 0 auto;
    cursor: pointer;
    font-weight: 600;
    border: 1px solid black;
    color: black;
    padding: 6px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    margin-top: 20px;
  }

  .start-button:hover {
      color: white;
      background-color: #42e048;
  }

  .loader {
    padding-top: 20px;
    margin: 0 auto;
    border: 5px solid #38373729; /* grey */
    border-top: 6px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 40px;
    height: 20px;
    animation: spin 2s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
}
</style>
