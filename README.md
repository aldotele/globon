<h2 align="center">
    Globon
</h2>

<p align="center">
  <img width="70" height="70" src="https://storage.googleapis.com/siteassetsswd/198/slideshow/663/20200625074107_56_o_1ba8en13b14c61b15hei1bd63jlc.jpg" alt="Material Bread logo">
</p>


1 . [Intro](#intro)\
2 . [Technology Stack](#technology-stack)\
3 . [API](#api)\
3 . [Run With Docker](#run-with-docker)

<br/>

### Intro
Globon lets you interact with the world map and locate areas of interest after applying filters.
For example, you can visualize the countries of the world within a specific population range, locate administrative capitals of a specific country, learn about different regions of the world, and a lot more.

<br/>

### Technology Stack
Back-End --> **Python** with **Django**\
Front-End --> **Vue.js**\
Database --> **PostgreSQL**\
Front-End hosting --> **Vercel**\
Back-End hosting --> **Render**

The project uses [Leaflet.js](https://leafletjs.com/) for map rendering and interaction.

<br/>

### API
The web application provides both REST and GraphQL endpoints that you can use for your own project.

They are available here:

[REST API](https://worldproxy.onrender.com/swagger)\
[GraphQL](https://worldproxy.onrender.com/graphql)

<br/>

### Run with Docker

`docker-compose up`

After the three containers are launched successfully, navigate to:

[localhost:5173](http://localhost:5173) to use Globon!

[localhost:8000/swagger](http://localhost:8000/swagger) to access the RESTful endpoints

[localhost:8000/graphql](http://localhost:8000/graphql) to access the GraphQL endpoint


