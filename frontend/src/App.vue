<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import WeatherHeader from './components/WeatherHeader.vue'
import SearchPanel from './components/SearchPanel.vue'
import MapPanel from './components/MapPanel.vue'
import WeatherSection from './components/WeatherSection.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import AuthPanel from './components/AuthPanel.vue'
import DashboardPanel from './components/DashboardPanel.vue'
import { apiDownload, apiRequest } from './api'

const STORAGE_KEYS = {
  language: 'weather-app.language',
  temperatureUnit: 'weather-app.temperature-unit',
}

const WEATHER_ICONS = {
  clear: '☀️',
  'partly-cloudy': '⛅',
  cloudy: '☁️',
  fog: '🌫️',
  drizzle: '🌦️',
  rain: '🌧️',
  showers: '🌦️',
  snow: '❄️',
  storm: '⛈️',
  unknown: '🌤️',
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
const isAuthenticated = ref(false)
const authUser = ref(null)
const isSearching = ref(false)
const isCurrentLocationLoading = ref(false)
const isDashboardLoading = ref(false)
const isAuthLoading = ref(false)
const weatherError = ref('')
const dashboardError = ref('')
const authError = ref('')

const currentWeather = reactive({
  location: 'San Francisco',
  region: 'California, United States',
  temperatureC: null,
  condition: 'Waiting for lookup',
  feelsLikeC: null,
  humidity: 'Humidity unavailable',
  wind: 'Wind unavailable',
  icon: '🌤️',
  latitude: null,
  longitude: null,
  source: '',
})

const forecastDays = ref([])
const savedWeatherRecords = ref([])
const rangeDays = ref([])
const rangeSummary = ref(null)

const customRange = reactive({
  startDate: '',
  endDate: '',
})

const formattedCurrentTemp = computed(() => formatTemperature(currentWeather.temperatureC, temperatureUnit.value))
const formattedFeelsLike = computed(() => {
  if (currentWeather.feelsLikeC == null) {
    return 'Feels like unavailable'
  }
  return `Feels like ${formatTemperature(currentWeather.feelsLikeC, temperatureUnit.value)}`
})
const formattedForecastDays = computed(() => forecastDays.value.map((item) => ({
  ...item,
  day: formatWeekday(item.date),
  dateLabel: formatDateLabel(item.date),
  temp: formatRangeTemperature(item.temp_min_c, item.temp_max_c, temperatureUnit.value),
  dayInfo: `${item.condition}${item.temp_max_c != null ? ` with highs near ${formatTemperature(item.temp_max_c, temperatureUnit.value)}` : ''}`,
  nightInfo: item.temp_min_c != null ? `Lows around ${formatTemperature(item.temp_min_c, temperatureUnit.value)}.` : 'Night details unavailable.',
})))
const formattedRangeDays = computed(() => rangeDays.value.map((item) => ({
  ...item,
  day: formatWeekday(item.date),
  dateLabel: formatDateLabel(item.date),
  temp: formatRangeTemperature(item.temp_min_c, item.temp_max_c, temperatureUnit.value),
  dayInfo: `${item.condition}${item.temp_max_c != null ? ` with highs near ${formatTemperature(item.temp_max_c, temperatureUnit.value)}` : ''}`,
  nightInfo: item.temp_min_c != null ? `Lows around ${formatTemperature(item.temp_min_c, temperatureUnit.value)}.` : 'Night details unavailable.',
})))
const formattedRangeSummary = computed(() => {
  if (!rangeSummary.value) {
    return null
  }

  return {
    ...rangeSummary.value,
    averageTemp: formatTemperature(rangeSummary.value.average_temp_c, temperatureUnit.value),
    maxTemp: formatTemperature(rangeSummary.value.max_temp_c, temperatureUnit.value),
    minTemp: formatTemperature(rangeSummary.value.min_temp_c, temperatureUnit.value),
  }
})

function formatTemperature(value, unit) {
  if (value == null || Number.isNaN(value)) {
    return '--'
  }

  if (unit === 'F') {
    return `${Math.round((value * 9) / 5 + 32)}°F`
  }

  return `${Math.round(value)}°C`
}

function formatRangeTemperature(minValue, maxValue, unit) {
  const low = formatTemperature(minValue, unit)
  const high = formatTemperature(maxValue, unit)
  if (low === '--' && high === '--') {
    return '--'
  }
  return `${low} to ${high}`
}

function formatWeekday(value) {
  return new Date(`${value}T00:00:00`).toLocaleDateString('en-US', { weekday: 'short' })
}

function formatDateLabel(value) {
  return new Date(`${value}T00:00:00`).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function weatherIcon(code) {
  return WEATHER_ICONS[code] ?? WEATHER_ICONS.unknown
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

function normalizeCurrentWeather(payload) {
  selectedLocation.value = payload.location.display_label
  currentWeather.location = payload.location.name
  currentWeather.region = [payload.location.region, payload.location.country].filter(Boolean).join(', ') || payload.location.display_label
  currentWeather.temperatureC = payload.current?.temperature_c ?? null
  currentWeather.condition = payload.current?.condition ?? 'Weather unavailable'
  currentWeather.feelsLikeC = payload.current?.feels_like_c ?? null
  currentWeather.humidity = payload.current?.humidity != null ? `Humidity ${Math.round(payload.current.humidity)}%` : 'Humidity unavailable'
  currentWeather.wind = payload.current?.wind_speed != null ? `Wind ${Math.round(payload.current.wind_speed)} km/h` : 'Wind unavailable'
  currentWeather.icon = weatherIcon(payload.current?.icon_code)
  currentWeather.latitude = payload.location.latitude
  currentWeather.longitude = payload.location.longitude
  currentWeather.source = payload.source
}

async function fetchCurrentWeather(location) {
  const payload = await apiRequest(`/weather/current?location=${encodeURIComponent(location)}`)
  normalizeCurrentWeather(payload)
  return payload
}

async function fetchForecast(location) {
  const payload = await apiRequest(`/weather/forecast?location=${encodeURIComponent(location)}&days=5`)
  forecastDays.value = payload.forecast_days
}

async function fetchHistory() {
  const payload = await apiRequest('/weather/history')
  savedWeatherRecords.value = payload.records.map((record) => ({
    id: record.id,
    location: record.resolved_name,
    startDate: record.start_date ?? 'Current weather',
    endDate: record.end_date ?? 'Current weather',
    temperature: historyTemperature(record.weather_payload),
    status: record.status,
    notes: record.notes,
  }))
}

function historyTemperature(payload) {
  if (payload?.current?.temperature_c != null) {
    return formatTemperature(payload.current.temperature_c, temperatureUnit.value)
  }
  if (payload?.range_summary?.average_temp_c != null) {
    return `Avg ${formatTemperature(payload.range_summary.average_temp_c, temperatureUnit.value)}`
  }
  return '--'
}

async function handleSearch(query) {
  searchQuery.value = query.trim()

  if (!searchQuery.value) {
    searchError.value = 'Please enter a location before searching.'
    statusText.value = 'Enter a location to see details'
    return
  }

  isSearching.value = true
  searchError.value = ''
  weatherError.value = ''
  rangeSummary.value = null
  rangeDays.value = []

  try {
    await fetchCurrentWeather(searchQuery.value)
    await fetchForecast(searchQuery.value)
    statusText.value = `Showing weather for ${selectedLocation.value}`
  } catch (error) {
    searchError.value = error.message || 'Unable to fetch weather for that location.'
    statusText.value = 'Location lookup failed'
  } finally {
    isSearching.value = false
  }
}

async function handleCurrentLocation() {
  if (!navigator.geolocation) {
    searchError.value = 'Your browser does not support current-location lookup.'
    return
  }

  isCurrentLocationLoading.value = true
  searchError.value = ''
  weatherError.value = ''
  rangeSummary.value = null
  rangeDays.value = []

  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 15000,
      })
    })
    const { latitude, longitude } = position.coords
    const payload = await apiRequest(`/weather/current-location?lat=${latitude}&lon=${longitude}`)
    normalizeCurrentWeather(payload)
    await fetchForecast(`${latitude}, ${longitude}`)
    statusText.value = `Showing weather for your current location`
  } catch (error) {
    searchError.value = error.message || 'Unable to determine your current location.'
    statusText.value = 'Current-location lookup failed'
  } finally {
    isCurrentLocationLoading.value = false
  }
}

function setActiveView(view) {
  activeView.value = view
}

async function handleRangeSubmit(payload) {
  customRange.startDate = payload.startDate
  customRange.endDate = payload.endDate

  if (!payload.startDate || !payload.endDate) {
    weatherError.value = 'Please choose both a start date and an end date.'
    return
  }

  weatherError.value = ''

  try {
    const targetLocation = searchQuery.value.trim() || selectedLocation.value
    const result = await apiRequest(`/weather/range?location=${encodeURIComponent(targetLocation)}&start_date=${payload.startDate}&end_date=${payload.endDate}`)
    rangeSummary.value = result.range_summary
    rangeDays.value = result.forecast_days
    selectedLocation.value = result.location.display_label
    currentWeather.region = [result.location.region, result.location.country].filter(Boolean).join(', ') || result.location.display_label
    currentWeather.latitude = result.location.latitude
    currentWeather.longitude = result.location.longitude
    statusText.value = `Custom range loaded for ${selectedLocation.value}`

    if (isAuthenticated.value) {
      await apiRequest('/weather/history', {
        method: 'POST',
        body: JSON.stringify({
          location: targetLocation,
          start_date: payload.startDate,
          end_date: payload.endDate,
          status: 'Saved',
        }),
      })
      await fetchHistory()
    }
  } catch (error) {
    weatherError.value = error.message || 'Unable to load custom range weather.'
  }
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
  authError.value = ''
  authMode.value = mode
  showAuthPanel.value = true
}

function closeAuth() {
  showAuthPanel.value = false
}

function switchAuthMode(mode) {
  authError.value = ''
  authMode.value = mode
}

async function submitAuth(payload) {
  isAuthLoading.value = true
  authError.value = ''

  try {
    const path = payload.mode === 'signin' ? '/auth/login' : '/auth/register'
    const result = await apiRequest(path, {
      method: 'POST',
      body: JSON.stringify({
        email: payload.email,
        password: payload.password,
      }),
    })
    authUser.value = result.user
    isAuthenticated.value = true
    showAuthPanel.value = false
    statusText.value = `${payload.mode === 'signin' ? 'Signed in' : 'Registered'} as ${result.user.email}`
    activePage.value = 'dashboard'
    await fetchHistory()
  } catch (error) {
    authError.value = error.message || 'Authentication failed.'
  } finally {
    isAuthLoading.value = false
  }
}

async function logout() {
  try {
    await apiRequest('/auth/logout', { method: 'POST' })
  } finally {
    isAuthenticated.value = false
    authUser.value = null
    savedWeatherRecords.value = []
    activePage.value = 'home'
    statusText.value = 'Signed out'
  }
}

async function openDashboard() {
  if (!isAuthenticated.value) {
    openAuth('signin')
    statusText.value = 'Sign in to open the dashboard'
    return
  }

  activePage.value = 'dashboard'
  isDashboardLoading.value = true
  dashboardError.value = ''

  try {
    await fetchHistory()
  } catch (error) {
    dashboardError.value = error.message || 'Unable to load saved weather records.'
  } finally {
    isDashboardLoading.value = false
  }
}

function backToHome() {
  activePage.value = 'home'
}

async function removeRecord(recordId) {
  try {
    await apiRequest(`/weather/history/${recordId}`, { method: 'DELETE' })
    savedWeatherRecords.value = savedWeatherRecords.value.filter((item) => item.id !== recordId)
    statusText.value = 'Record deleted'
  } catch (error) {
    dashboardError.value = error.message || 'Unable to delete that record.'
  }
}

async function exportRecords(format) {
  try {
    const response = await apiDownload(`/weather/export?format=${format}`)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `weather-history.${format === 'markdown' ? 'md' : format}`
    document.body.appendChild(anchor)
    anchor.click()
    anchor.remove()
    window.URL.revokeObjectURL(url)
    statusText.value = `Exported records as ${format.toUpperCase()}`
  } catch (error) {
    dashboardError.value = error.message || 'Unable to export records.'
  }
}

async function updateRecord(recordId) {
  const target = savedWeatherRecords.value.find((item) => item.id === recordId)
  if (!target) {
    return
  }

  const nextStatus = target.status === 'Active' ? 'Saved' : 'Active'

  try {
    await apiRequest(`/weather/history/${recordId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status: nextStatus }),
    })
    target.status = nextStatus
    statusText.value = `Record marked as ${nextStatus}`
  } catch (error) {
    dashboardError.value = error.message || 'Unable to update that record.'
  }
}

async function loadAuthState() {
  try {
    const payload = await apiRequest('/auth/me')
    authUser.value = payload.user
    isAuthenticated.value = true
  } catch {
    authUser.value = null
    isAuthenticated.value = false
  }
}

watch(temperatureUnit, () => {
  savedWeatherRecords.value = savedWeatherRecords.value.map((record) => ({
    ...record,
    temperature: historyTemperature(record.weather_payload),
  }))
})

onMounted(async () => {
  loadSettings()
  window.addEventListener('keydown', handleGlobalKeydown)
  await loadAuthState()
  await handleSearch(selectedLocation.value)
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
      :is-authenticated="isAuthenticated"
      :user-email="authUser?.email ?? ''"
      @open-settings="openSettings"
      @open-auth="openAuth('signin')"
      @open-dashboard="openDashboard"
      @home="backToHome"
      @logout="logout"
    />

    <template v-if="activePage === 'home'">
      <main class="top-grid">
        <SearchPanel
          v-model:query="searchQuery"
          :error-message="searchError"
          :loading="isSearching"
          :current-location-loading="isCurrentLocationLoading"
          @search="handleSearch"
          @use-current-location="handleCurrentLocation"
        />

        <MapPanel
          :location-label="selectedLocation"
          :region-label="currentWeather.region"
          :latitude="currentWeather.latitude"
          :longitude="currentWeather.longitude"
        />
      </main>

      <WeatherSection
        :active-view="activeView"
        :selected-location="selectedLocation"
        :current-weather="currentWeather"
        :forecast-days="formattedForecastDays"
        :custom-range="customRange"
        :range-days="formattedRangeDays"
        :range-summary="formattedRangeSummary"
        :temperature-unit="temperatureUnit"
        :current-temperature="formattedCurrentTemp"
        :feels-like-text="formattedFeelsLike"
        :error-message="weatherError"
        @change-view="setActiveView"
        @submit-range="handleRangeSubmit"
      />
    </template>

    <DashboardPanel
      v-else
      :records="savedWeatherRecords"
      :temperature-unit="temperatureUnit"
      :loading="isDashboardLoading"
      :error-message="dashboardError"
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
      :loading="isAuthLoading"
      :error-message="authError"
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
