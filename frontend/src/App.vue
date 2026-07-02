<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import WeatherHeader from './components/WeatherHeader.vue'
import SearchPanel from './components/SearchPanel.vue'
import MapPanel from './components/MapPanel.vue'
import WeatherSection from './components/WeatherSection.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import AuthPanel from './components/AuthPanel.vue'
import DashboardPanel from './components/DashboardPanel.vue'

const STORAGE_KEYS = {
  language: 'weather-app.language',
  temperatureUnit: 'weather-app.temperature-unit',
}

const activeView = ref('now')
const selectedLocation = ref('San Francisco')
const statusText = ref('Enter a location to see details')
const searchQuery = ref('')
const searchError = ref('')
const showSettings = ref(false)
const showAuthPanel = ref(false)
const authMode = ref('signin')
const temperatureUnit = ref('C')
const language = ref('English')
const activePage = ref('home')

const currentWeather = reactive({
  location: 'San Francisco',
  region: 'California, United States',
  temperatureC: 24,
  condition: 'Clear sky',
  feelsLikeC: 23,
  humidity: 'Humidity 61%',
  wind: 'Wind 8 km/h',
  icon: '☀️',
})

const forecastDays = [
  { day: 'Mon', date: 'Jun 2', tempC: 24, condition: 'Sunny', dayInfo: 'Warm and clear through most of the day.', nightInfo: 'Cool and calm overnight with clear skies.' },
  { day: 'Tue', date: 'Jun 3', tempC: 22, condition: 'Cloudy', dayInfo: 'Overcast daytime with mild temperatures.', nightInfo: 'Cloud cover remains through the night.' },
  { day: 'Wed', date: 'Jun 4', tempC: 19, condition: 'Light Rain', dayInfo: 'Light showers in the afternoon.', nightInfo: 'Rain tapers off by late evening.' },
  { day: 'Thu', date: 'Jun 5', tempC: 21, condition: 'Partly Cloudy', dayInfo: 'Mixed sun and clouds during the day.', nightInfo: 'Mild night with some cloud cover.' },
  { day: 'Fri', date: 'Jun 6', tempC: 25, condition: 'Clear', dayInfo: 'Bright and dry with good visibility.', nightInfo: 'Clear skies and light winds overnight.' },
]

const savedWeatherRecords = ref([
  {
    id: 1,
    location: 'San Francisco',
    startDate: '2026-06-01',
    endDate: '2026-06-05',
    temperature: '24°C',
    status: 'Active',
  },
  {
    id: 2,
    location: 'Tokyo',
    startDate: '2026-06-10',
    endDate: '2026-06-15',
    temperature: '29°C',
    status: 'Saved',
  },
])

const customRange = reactive({
  startDate: '',
  endDate: '',
})

const formattedCurrentTemp = computed(() => formatTemperature(currentWeather.temperatureC, temperatureUnit.value))
const formattedFeelsLike = computed(() => `Feels like ${formatTemperature(currentWeather.feelsLikeC, temperatureUnit.value)}`)
const formattedForecastDays = computed(() => forecastDays.map((item) => ({
  ...item,
  temp: formatTemperature(item.tempC, temperatureUnit.value),
})))

function formatTemperature(value, unit) {
  if (unit === 'F') {
    return `${Math.round((value * 9) / 5 + 32)}°F`
  }

  return `${value}°C`
}

function readStorage(key, fallback) {
  try {
    return window.localStorage.getItem(key) ?? fallback
  } catch {
    return fallback
  }
}

function writeStorage(key, value) {
  try {
    window.localStorage.setItem(key, value)
  } catch {
    // Ignore storage errors in private/incognito contexts.
  }
}

function loadSettings() {
  language.value = readStorage(STORAGE_KEYS.language, language.value)
  temperatureUnit.value = readStorage(STORAGE_KEYS.temperatureUnit, temperatureUnit.value)
}

function handleGlobalKeydown(event) {
  if (event.key !== 'Escape') {
    return
  }

  if (showAuthPanel.value) {
    closeAuth()
    return
  }

  if (showSettings.value) {
    closeSettings()
  }
}

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

function openSettings() {
  showSettings.value = true
}

function closeSettings() {
  showSettings.value = false
}

function saveSettings(payload) {
  temperatureUnit.value = payload.temperatureUnit
  language.value = payload.language
  writeStorage(STORAGE_KEYS.language, language.value)
  writeStorage(STORAGE_KEYS.temperatureUnit, temperatureUnit.value)
  showSettings.value = false
  statusText.value = `Settings updated: ${language.value}, ${temperatureUnit.value}`
}

function openAuth(mode) {
  authMode.value = mode
  showAuthPanel.value = true
}

function closeAuth() {
  showAuthPanel.value = false
}

function switchAuthMode(mode) {
  authMode.value = mode
}

function submitAuth(payload) {
  statusText.value = `${payload.mode === 'signin' ? 'Signed in' : 'Registered'} in ${language.value}`
  activePage.value = 'dashboard'
  showAuthPanel.value = false
}

function openDashboard() {
  activePage.value = 'dashboard'
}

function backToHome() {
  activePage.value = 'home'
}

function removeRecord(recordId) {
  savedWeatherRecords.value = savedWeatherRecords.value.filter((item) => item.id !== recordId)
}

function exportRecords(format) {
  statusText.value = `Exporting records as ${format.toUpperCase()}`
}

function updateRecord(recordId) {
  statusText.value = `Update requested for record ${recordId}`
}

onMounted(() => {
  loadSettings()
  window.addEventListener('keydown', handleGlobalKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<template>
  <div class="page-shell">
    <WeatherHeader
      :selected-location="selectedLocation"
      :status-text="statusText"
      :temperature-unit="temperatureUnit"
      @open-settings="openSettings"
      @open-auth="openAuth('signin')"
      @open-dashboard="openDashboard"
      @home="backToHome"
    />

    <template v-if="activePage === 'home'">
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
        :forecast-days="formattedForecastDays"
        :custom-range="customRange"
        :temperature-unit="temperatureUnit"
        :current-temperature="formattedCurrentTemp"
        :feels-like-text="formattedFeelsLike"
        @change-view="setActiveView"
        @submit-range="handleRangeSubmit"
      />
    </template>

    <DashboardPanel
      v-else
      :records="savedWeatherRecords"
      :temperature-unit="temperatureUnit"
      @back="backToHome"
      @update-record="updateRecord"
      @delete-record="removeRecord"
      @export-records="exportRecords"
    />

    <SettingsPanel
      v-if="showSettings"
      :language="language"
      :temperature-unit="temperatureUnit"
      @close="closeSettings"
      @save="saveSettings"
    />

    <AuthPanel
      v-if="showAuthPanel"
      :mode="authMode"
      @close="closeAuth"
      @switch-mode="switchAuthMode"
      @submit="submitAuth"
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
  background: #f5f8f4;
  color: #17311f;
}

:global(button),
:global(input),
:global(select) {
  font: inherit;
}

.page-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 24px auto 40px;
  display: grid;
  gap: 20px;
  position: relative;
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
