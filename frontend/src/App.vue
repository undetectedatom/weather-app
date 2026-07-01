<script setup>
import { reactive, ref } from 'vue'
import WeatherHeader from './components/WeatherHeader.vue'
import SearchPanel from './components/SearchPanel.vue'
import MapPanel from './components/MapPanel.vue'
import WeatherSection from './components/WeatherSection.vue'

const activeView = ref('now')
const selectedLocation = ref('San Francisco')
const statusText = ref('Enter a location to see details')
const searchQuery = ref('')
const searchError = ref('')

const currentWeather = reactive({
  location: 'San Francisco',
  region: 'California, United States',
  temperature: '24°C',
  condition: 'Clear sky',
  feelsLike: 'Feels like 23°C',
  humidity: 'Humidity 61%',
  wind: 'Wind 8 km/h',
  icon: '☀️',
})

const forecastDays = [
  {
    day: 'Mon',
    date: 'Jun 2',
    temp: '24°C',
    condition: 'Sunny',
    dayInfo: 'Warm and clear through most of the day.',
    nightInfo: 'Cool and calm overnight with clear skies.',
  },
  {
    day: 'Tue',
    date: 'Jun 3',
    temp: '22°C',
    condition: 'Cloudy',
    dayInfo: 'Overcast daytime with mild temperatures.',
    nightInfo: 'Cloud cover remains through the night.',
  },
  {
    day: 'Wed',
    date: 'Jun 4',
    temp: '19°C',
    condition: 'Light Rain',
    dayInfo: 'Light showers in the afternoon.',
    nightInfo: 'Rain tapers off by late evening.',
  },
  {
    day: 'Thu',
    date: 'Jun 5',
    temp: '21°C',
    condition: 'Partly Cloudy',
    dayInfo: 'Mixed sun and clouds during the day.',
    nightInfo: 'Mild night with some cloud cover.',
  },
  {
    day: 'Fri',
    date: 'Jun 6',
    temp: '25°C',
    condition: 'Clear',
    dayInfo: 'Bright and dry with good visibility.',
    nightInfo: 'Clear skies and light winds overnight.',
  },
]

const customRange = reactive({
  startDate: '',
  endDate: '',
})

function handleSearch(query) {
  searchQuery.value = query.trim()

  if (!searchQuery.value) {
    searchError.value = 'Please enter a location before searching.'
    statusText.value = 'Enter a location to see details'
    return
  }

  searchError.value = ''
  selectedLocation.value = searchQuery.value
  currentWeather.location = searchQuery.value
  statusText.value = `Showing results for ${searchQuery.value}`
}

function setActiveView(view) {
  activeView.value = view
}

function handleRangeSubmit(payload) {
  customRange.startDate = payload.startDate
  customRange.endDate = payload.endDate
  statusText.value = `Custom range selected for ${selectedLocation.value}`
}
</script>

<template>
  <div class="page-shell">
    <WeatherHeader
      :selected-location="selectedLocation"
      :status-text="statusText"
    />

    <main class="top-grid">
      <SearchPanel
        v-model:query="searchQuery"
        :error-message="searchError"
        @search="handleSearch"
      />

      <MapPanel :location-label="selectedLocation" />
    </main>

    <WeatherSection
      :active-view="activeView"
      :selected-location="selectedLocation"
      :current-weather="currentWeather"
      :forecast-days="forecastDays"
      :custom-range="customRange"
      @change-view="setActiveView"
      @submit-range="handleRangeSubmit"
    />
  </div>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background:
    radial-gradient(circle at top, rgba(101, 163, 255, 0.18), transparent 34%),
    linear-gradient(180deg, #f4f8ff 0%, #eef3fa 100%);
  color: #10233f;
}

:global(button),
:global(input) {
  font: inherit;
}

.page-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 24px auto 40px;
  display: grid;
  gap: 20px;
}

.top-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
  gap: 20px;
}

@media (max-width: 960px) {
  .top-grid {
    grid-template-columns: 1fr;
  }
}
</style>
