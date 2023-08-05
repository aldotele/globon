<script setup>
import { RouterLink } from 'vue-router';


</script>

<template>
    <header>
        <nav class="container">
            <div class="branding">
                <img src="../assets/globon-icon.png" alt="">
                <h1>Globon</h1>
            </div>
            <ul class="nav-routes">
                <RouterLink to="/">Home</RouterLink>
                <RouterLink to="/about">About</RouterLink>
            </ul>
        </nav>
    </header>
</template>


<style lang="scss" scoped>
header {
  nav {
    display: flex;
    align-items: center;
    padding: 25px 16px;
    border-bottom: 2px solid rgb(208, 206, 206);

    .branding {
      display: flex;
      align-items: center;
      gap: 8px;
      img {
        max-width: 50px;
      }

      h1 {
        font-size: 24px;
      }
    }

    .nav-routes {
      display: flex;
      flex: 1;
      justify-content: flex-end;
      gap: 12px;
      list-style: none;

      a {
        text-decoration: none;
        color: inherit;
      }
    }
  }
}
</style>