<script setup></script>

<template>
  <div class="header">
    <div class="header-left">
      <button>
        HellowWeather
      </button>
    </div>
    <div class="header-middle">
      <!-- dynamically show the location -->
      <!-- Before entering a location: Enter a location to see details
      After entering the wrong location: Invalid location
      With the correct location: Show the location name -->
    </div>
    <div class="header-right">
      <button>
        Settings
      </button>

      <button>
        Sign In
      </button>
    </div>


  </div>
  <div class="location">
    <div class="location-selection">
      <div class="introduction">
        <!-- introduction to how to search  -->
      </div>
      <div class="location-search">
        <form action="">
          <input type="text">
          <input type="button" value="submit">
        </form>
      </div>
    </div>
    <div class="map">
      This is a map.
    </div>
  </div>
  <div class="weather-display">
    <div class="time-selection">
      <ul>
        <li>Now</li>
        <li>7 Day</li>
        <li>Custom range</li>
      </ul>

    </div>
    <!-- If select now -->
    <div class="weather-now">
      <div class="info-card">
        <div class="info-header">
          Location<!-- dynamically showing current location -->
        </div>
        <div class="info-content">
          <!-- dynamically showing current weather info -->
        </div>
      </div>
      <div class="info-card">
        <div class="info-header">
          Weather Forecast
        </div>
        <div class="info-content">
          <!-- dynamically showing Tomorrow weather info -->
        </div>
      </div>
    </div>
    <div class="weather-week">
      <div class="foldable-item">
        <div class="foldable-header">
          <!-- This contains an unfold button, default to fold -->
          Tue, Jun 3
          <button>icon like /\ or \/</button>
        </div>
        <div class="foldable-detail">
          <div class="day">
            Show weather forecast in daytime
          </div>
          <div class="night">
            Show weather forecast in night
          </div>
        </div>
      </div>
    </div>


  </div>

</template>

<style scoped>
.header {
  background-color: aquamarine;
  margin-bottom: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

ul {
  list-style-type: none;
  padding-left: 0;
  margin-left: 0;
}

.location {
  display: flex;
  justify-content: space-around;
}

.weather-display {
  width: 600px;
  background-color: aqua;
}

.time-selection {
  width: 250px
}

.time-selection>ul {
  display: flex;
  justify-content: space-between;
}

.map {
  width: 350px;
  height: 300px;
  background-color: bisque;
}

.weather-now {
  display: flex;
  flex: auto auto 1;
}

.info-card {
  width: 200px;
  height: 200px;
  background-color: aliceblue;
  border: 2px solid black;
  border-radius: 10px;
  padding: 20px;
}

.info-header {
  text-align: center;
}

.weather-week {
  display: flex;
}

.foldable-item {
  display: flex;
  flex-direction: column;
}

.foldable-detail {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
