<h2 align="center">
    Globon
</h2>

<p align="center">
  <img width="70" height="70" src="https://storage.googleapis.com/siteassetsswd/198/slideshow/663/20200625074107_56_o_1ba8en13b14c61b15hei1bd63jlc.jpg" alt="Material Bread logo">
</p>


1 . [Intro](#intro)\
1 . [Technology Stack](#technology-stack)\
2 . [Run With Docker](#run-with-docker)

<br/>

### Intro
The Globon WebApp allows you to visualize the world map and locate countries of the world, after applying filters on them.
For example, you can visualize the countries of the world within a specific population range.\

<br/>

### Technology Stack
The project uses Angular (with Leaflet.js for map visualization) on the client side, 
Javalin (lightweight Java framework) on the server side
and MongoDB with geospatial features as a database.

<br/>

### Run with Docker

`docker-compose up`

After the three containers are launched successfully, navigate to:
[http://localhost:4200]()

You can also access the available enpoints on [http://localhost:7070/swagger]()

