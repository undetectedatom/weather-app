<template>
  <section class="panel weather-panel">
    <div class="section-heading section-heading-row">
      <div>
        <p class="eyebrow">{{ labels.eyebrow }}</p>
        <h2>{{ labels.title }}</h2>
      </div>
      <nav class="time-selection" aria-label="Weather range">
        <button type="button" :class="{ active: activeView === 'now' }" @click="$emit('change-view', 'now')">{{ labels.now }}</button>
        <button type="button" :class="{ active: activeView === 'forecast' }" @click="$emit('change-view', 'forecast')">{{ labels.forecast }}</button>
        <button type="button" :class="{ active: activeView === 'customRange' }" @click="$emit('change-view', 'customRange')">{{ labels.customRange }}</button>
      </nav>
    </div>

    <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

    <div v-if="activeView === 'now'" class="summary-grid">
      <article class="info-card highlight-card current-card">
        <div class="info-header">{{ labels.currentWeather }}</div>
        <div class="info-content current-content">
          <div class="weather-icon">{{ currentWeather.icon }}</div>
          <div class="headline-block">
            <strong>{{ currentTemperature }}</strong>
            <p class="condition-text">{{ currentWeather.condition }}</p>
            <p v-if="selectedLocation" class="location-text">{{ selectedLocation }}</p>
          </div>
        </div>
      </article>
      <article class="info-card details-card">
        <div class="info-header">{{ labels.usefulDetails }}</div>
        <div class="info-content details-grid">
          <div class="detail-pill"><span>🌡️</span><p>{{ feelsLikeText }}</p></div>
          <div class="detail-pill"><span>💧</span><p>{{ currentWeather.humidity }}</p></div>
          <div class="detail-pill"><span>🌬️</span><p>{{ currentWeather.wind }}</p></div>
          <div class="detail-pill"><span>📈</span><p>{{ todayRangeText }}</p></div>
        </div>
      </article>
    </div>

    <section v-else-if="activeView === 'customRange'" class="custom-range-card">
      <div class="section-heading">
        <p class="eyebrow">{{ labels.customEyebrow }}</p>
        <h2>{{ labels.customTitle }}</h2>
      </div>
      <form class="range-form" @submit.prevent="submitRange">
        <label><span>{{ labels.startDate }}</span><input v-model="startDate" class="date-input" type="date" :disabled="rangeLoading" @focus="ensureDateInputVisible" /></label>
        <label><span>{{ labels.endDate }}</span><input v-model="endDate" class="date-input" type="date" :disabled="rangeLoading" @focus="ensureDateInputVisible" /></label>
        <button type="submit" :disabled="rangeLoading">{{ rangeLoading ? labels.checkingRange : labels.checkRange }}</button>
      </form>
      <section v-if="rangeDays.length" class="weather-list-shell">
        <div class="weather-list-header">
          <div>
            <p class="eyebrow">{{ labels.customEyebrow }}</p>
            <h3>{{ labels.checkRangeTitle }}</h3>
          </div>
          <div v-if="rangeSummary" class="range-summary-card">
            <strong>{{ rangeSummary.start_date }} to {{ rangeSummary.end_date }}</strong>
            <p>{{ labels.average }} {{ rangeSummary.averageTemp }}</p>
            <p>{{ labels.highLow }} {{ rangeSummary.maxTemp }} / Low {{ rangeSummary.minTemp }}</p>
          </div>
        </div>
        <section v-if="showRangeTrend" class="trend-card range-trend-card">
          <div class="trend-header">
            <p class="eyebrow">{{ labels.trend }}</p>
            <p>{{ labels.average }}</p>
          </div>
          <TrendChart
            :labels="rangeChartLabels"
            :values="rangeChartValues"
            line-color="#2f7d4b"
            fill-top="rgba(47, 125, 75, 0.26)"
            fill-bottom="rgba(47, 125, 75, 0.02)"
          />
        </section>
        <section class="forecast-list">
          <article v-for="item in rangeDays" :key="item.date" class="forecast-card">
            <details>
              <summary>
                <div class="forecast-summary">
                  <div class="forecast-day">
                    <div class="forecast-day-copy"><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
                    <span class="forecast-icon">{{ item.icon }}</span>
                  </div>
                  <div class="forecast-meta">
                    <span class="forecast-condition">{{ item.condition }}</span>
                    <span class="forecast-temp">{{ item.temp }}</span>
                    <span class="forecast-average">{{ labels.average }} {{ item.averageTempLabel }}</span>
                  </div>
                </div>
              </summary>
              <div class="forecast-detail-grid">
                <div class="forecast-detail-card">
                  <p class="detail-label">☀️ {{ labels.day }}</p>
                  <p>{{ item.dayInfo }}</p>
                </div>
                <div class="forecast-detail-card">
                  <p class="detail-label">🌙 {{ labels.night }}</p>
                  <p>{{ item.nightInfo }}</p>
                </div>
                <div class="forecast-detail-card">
                  <p class="detail-label">📈 {{ labels.highLow }}</p>
                  <p>{{ item.highTempLabel }}</p>
                </div>
                <div class="forecast-detail-card">
                  <p class="detail-label">📉 Low</p>
                  <p>{{ item.lowTempLabel }}</p>
                </div>
                <div class="forecast-detail-card">
                  <p class="detail-label">🧭 {{ labels.average }}</p>
                  <p>{{ item.averageTempLabel }}</p>
                </div>
                <div class="forecast-detail-card">
                  <p class="detail-label">🌤️ Condition</p>
                  <p>{{ item.condition }}</p>
                </div>
              </div>
            </details>
          </article>
        </section>
      </section>
    </section>

    <section v-else class="weather-list-shell">
      <div class="weather-list-header">
        <h3>{{ labels.forecast }}</h3>
      </div>
      <section v-if="showForecastTrend" class="trend-card forecast-trend-card">
        <div class="trend-header">
          <p class="eyebrow">{{ labels.trend }}</p>
          <p>{{ labels.average }}</p>
        </div>
        <TrendChart
          :labels="forecastChartLabels"
          :values="forecastChartValues"
          line-color="#d27b2c"
          fill-top="rgba(210, 123, 44, 0.24)"
          fill-bottom="rgba(210, 123, 44, 0.02)"
        />
      </section>
      <section class="forecast-list">
        <article v-for="item in forecastDays" :key="item.date" class="forecast-card">
          <details>
            <summary>
              <div class="forecast-summary">
                <div class="forecast-day">
                  <div class="forecast-day-copy"><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
                  <span class="forecast-icon">{{ item.icon }}</span>
                </div>
                <div class="forecast-meta">
                  <span class="forecast-condition">{{ item.condition }}</span>
                  <span class="forecast-temp">{{ item.temp }}</span>
                  <span class="forecast-average">{{ labels.average }} {{ item.averageTempLabel }}</span>
                </div>
              </div>
            </summary>
            <div class="forecast-detail-grid">
              <div class="forecast-detail-card">
                <p class="detail-label">☀️ {{ labels.day }}</p>
                <p>{{ item.dayInfo }}</p>
              </div>
              <div class="forecast-detail-card">
                <p class="detail-label">🌙 {{ labels.night }}</p>
                <p>{{ item.nightInfo }}</p>
              </div>
              <div class="forecast-detail-card">
                <p class="detail-label">📈 {{ labels.highLow }}</p>
                <p>{{ item.highTempLabel }}</p>
              </div>
              <div class="forecast-detail-card">
                <p class="detail-label">📉 Low</p>
                <p>{{ item.lowTempLabel }}</p>
              </div>
              <div class="forecast-detail-card">
                <p class="detail-label">🧭 {{ labels.average }}</p>
                <p>{{ item.averageTempLabel }}</p>
              </div>
              <div class="forecast-detail-card">
                <p class="detail-label">🌤️ Condition</p>
                <p>{{ item.condition }}</p>
              </div>
            </div>
          </details>
        </article>
      </section>
    </section>
  </section>
</template>

<script setup>
import TrendChart from './TrendChart.vue'
import { computed, ref, watch } from 'vue'

const props = defineProps({
  activeView: { type: String, required: true },
  selectedLocation: { type: String, required: true },
  currentWeather: { type: Object, required: true },
  forecastDays: { type: Array, required: true },
  customRange: { type: Object, required: true },
  rangeDays: { type: Array, default: () => [] },
  rangeSummary: { type: Object, default: null },
  currentTemperature: { type: String, required: true },
  feelsLikeText: { type: String, required: true },
  todayRangeText: { type: String, required: true },
  errorMessage: { type: String, default: '' },
  labels: { type: Object, required: true },
  rangeLoading: { type: Boolean, default: false },
})

const emit = defineEmits(['change-view', 'submit-range'])
const startDate = ref(props.customRange.startDate)
const endDate = ref(props.customRange.endDate)

watch(() => props.customRange.startDate, (value) => { startDate.value = value })
watch(() => props.customRange.endDate, (value) => { endDate.value = value })

const showRangeTrend = computed(() => props.rangeDays.length >= 2)
const showForecastTrend = computed(() => props.forecastDays.length >= 2)
const rangeChartLabels = computed(() => props.rangeDays.map((item) => item.dateLabel))
const forecastChartLabels = computed(() => props.forecastDays.map((item) => item.dateLabel))
const rangeChartValues = computed(() => sanitizeTrendValues(props.rangeDays))
const forecastChartValues = computed(() => sanitizeTrendValues(props.forecastDays))

function sanitizeTrendValues(items) {
  return items.map((item) => item.averageTempValue ?? null)
}

function ensureDateInputVisible(event) {
  if (window.innerWidth > 640) return
  event.target.scrollIntoView({ block: 'center', behavior: 'smooth' })
}

function submitRange() {
  emit('submit-range', { startDate: startDate.value, endDate: endDate.value })
}
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.weather-panel { display: grid; gap: 18px; }
.section-heading { display: grid; gap: 4px; }
.section-heading-row { grid-template-columns: 1fr auto; align-items: center; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, h3, p { margin: 0; }
.error-banner { border: 1px solid #e4bbbb; border-radius: 12px; padding: 12px 14px; background: #fff4f4; color: #a63a3a; }
.time-selection { display: flex; flex-wrap: wrap; gap: 8px; }
.time-selection button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 10px 14px; cursor: pointer; background: #ffffff; color: #23402e; }
.time-selection .active { background: #edf5ef; border-color: #7ab48a; color: #2f7d4b; }
.summary-grid { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr); gap: 14px; }
.info-card, .forecast-card, .custom-range-card, .range-summary-card, .trend-card { border-radius: 14px; border: 1px solid #cfd8cf; background: white; padding: 16px; }
.highlight-card, .range-summary-card { background: #f5faf6; }
.info-header { font-size: 0.9rem; color: #6f8174; margin-bottom: 10px; }
.info-content { display: grid; gap: 8px; }
.current-card { min-height: 100%; }
.current-content { grid-template-columns: auto 1fr; align-items: center; gap: 16px; }
.headline-block { display: grid; gap: 6px; }
.weather-icon { font-size: 3rem; line-height: 1; }
.headline-block strong { font-size: clamp(2rem, 4vw, 3rem); line-height: 1; }
.condition-text { color: #23402e; font-weight: 600; }
.location-text { color: #567061; }
.details-card { align-content: start; }
.details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.detail-pill { display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 10px; border: 1px solid #dbe4dc; border-radius: 12px; background: #f7faf7; padding: 12px; }
.detail-pill span { font-size: 1.1rem; }
.detail-pill p { color: #23402e; }
.custom-range-card, .weather-list-shell { display: grid; gap: 14px; }
.weather-list-header { display: flex; align-items: start; justify-content: space-between; gap: 14px; }
.range-summary-card { display: grid; gap: 6px; min-width: min(320px, 100%); }
.range-form { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; align-items: end; }
.range-form label { display: grid; gap: 6px; }
.range-form input, .range-form button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 12px 14px; }
.range-form button { cursor: pointer; background: #2f7d4b; border-color: #7ab48a; color: #fff; }
.range-form button:disabled, .range-form input:disabled { cursor: wait; opacity: 0.72; }
.trend-card { display: grid; gap: 10px; padding: 18px; }
.range-trend-card { background: linear-gradient(180deg, #f5faf6 0%, #ffffff 100%); }
.forecast-trend-card { background: linear-gradient(180deg, #fff7ef 0%, #ffffff 100%); }
.trend-header { display: flex; justify-content: space-between; gap: 12px; color: #4f6754; }
.forecast-list { display: grid; gap: 12px; }
.forecast-card details { display: grid; gap: 14px; }
.forecast-card { overflow: hidden; transition: border-color 160ms ease, box-shadow 160ms ease, background-color 160ms ease, transform 160ms ease; }
.forecast-card summary { list-style: none; cursor: pointer; padding: 4px; margin: -4px; border-radius: 12px; transition: background-color 160ms ease; }
.forecast-card summary::-webkit-details-marker { display: none; }
.forecast-card summary:hover { background: #f7faf7; }
.forecast-card summary:active { background: #eef6ef; }
.forecast-card:has(details[open]) { background: linear-gradient(180deg, #f8fbf8 0%, #ffffff 100%); border-color: #b8cdbd; box-shadow: 0 12px 28px rgba(35, 64, 46, 0.08); }
.forecast-card details[open] summary { background: #eef6ef; }
.forecast-summary { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
.forecast-day { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 12px; }
.forecast-day-copy { display: grid; gap: 2px; }
.forecast-icon { font-size: 1.8rem; line-height: 1; align-self: center; }
.forecast-meta { display: grid; gap: 4px; justify-items: end; text-align: right; }
.forecast-condition { color: #4f6754; }
.forecast-temp { font-weight: 700; }
.forecast-average { color: #567061; font-size: 0.92rem; }
.forecast-card p, .detail-label { color: #567061; }
.forecast-detail-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.forecast-detail-card { border: 1px solid #dbe4dc; border-radius: 12px; background: #fcfefd; padding: 12px; display: grid; gap: 6px; }
@media (max-width: 960px) {
  .summary-grid, .range-form, .forecast-detail-grid, .section-heading-row { grid-template-columns: 1fr; }
  .details-grid { grid-template-columns: 1fr; }
  .weather-list-header { flex-direction: column; }
}
@media (max-width: 640px) {
  .forecast-summary { align-items: start; }
  .forecast-meta { justify-items: start; text-align: left; }
}
</style>
