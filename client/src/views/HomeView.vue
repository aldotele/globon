<script setup>
import router from "@/router";

let isReady = false;

// contacting the server
const launch = () => {
  fetch("http://localhost:8000/ready/", { method: 'GET', redirect: 'follow'})
    .then(response => {
        response.json().then(json => {
            if (json['ready']) {
              isReady = true;
              console.log('ready')
              router.push("/countries");
            }
        })
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
