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
            <p v-if="currentWeather.region" class="region-text">{{ currentWeather.region }}</p>
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
        <label><span>{{ labels.startDate }}</span><input v-model="startDate" type="date" :disabled="rangeLoading" /></label>
        <label><span>{{ labels.endDate }}</span><input v-model="endDate" type="date" :disabled="rangeLoading" /></label>
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
        <section v-if="showRangeTrend" class="trend-card">
          <div class="trend-header">
            <p class="eyebrow">{{ labels.trend }}</p>
            <p>{{ labels.average }}</p>
          </div>
          <svg viewBox="0 0 100 44" class="trend-chart" preserveAspectRatio="none" aria-hidden="true">
            <defs>
              <linearGradient id="rangeTrendFill" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#2f7d4b" stop-opacity="0.28" />
                <stop offset="100%" stop-color="#2f7d4b" stop-opacity="0.02" />
              </linearGradient>
            </defs>
            <path class="trend-area" :d="rangeTrendAreaPath" />
            <path class="trend-line" :d="rangeTrendPath" />
            <circle v-for="point in rangeTrendDots" :key="point.key" class="trend-dot" :cx="point.x" :cy="point.y" r="1.6" />
          </svg>
          <div class="trend-labels">
            <span>{{ rangeDays[0]?.dateLabel }}</span>
            <span>{{ rangeDays[rangeDays.length - 1]?.dateLabel }}</span>
          </div>
        </section>
        <section class="forecast-list">
          <article v-for="item in rangeDays" :key="item.date" class="forecast-card">
            <details>
              <summary>
                <div class="forecast-summary">
                  <div class="forecast-day">
                    <div><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
                  </div>
                  <div class="forecast-meta">
                    <span class="forecast-condition">{{ item.condition }}</span>
                    <span class="forecast-temp">{{ item.temp }}</span>
                    <span class="forecast-average">{{ labels.average }} {{ item.averageTempLabel }}</span>
                    <span class="forecast-icon">{{ item.icon }}</span>
                  </div>
                </div>
              </summary>
              <div class="forecast-detail-grid">
                <div><p class="detail-label">{{ labels.day }}</p><p>{{ item.dayInfo }}</p></div>
                <div><p class="detail-label">{{ labels.night }}</p><p>{{ item.nightInfo }}</p></div>
              </div>
            </details>
          </article>
        </section>
      </section>
    </section>

    <section v-else class="weather-list-shell">
      <div class="weather-list-header">
        <div>
          <p class="eyebrow">{{ labels.forecast }}</p>
          <h3>{{ labels.title }}</h3>
        </div>
      </div>
      <section class="trend-card">
        <div class="trend-header">
          <p class="eyebrow">{{ labels.trend }}</p>
          <p>{{ labels.average }}</p>
        </div>
        <svg viewBox="0 0 100 44" class="trend-chart" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <linearGradient id="forecastTrendFill" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#d27b2c" stop-opacity="0.28" />
              <stop offset="100%" stop-color="#d27b2c" stop-opacity="0.02" />
            </linearGradient>
          </defs>
          <path class="trend-area forecast-trend-area" :d="forecastTrendAreaPath" />
          <path class="trend-line forecast-trend-line" :d="forecastTrendPath" />
          <circle v-for="point in forecastTrendDots" :key="point.key" class="trend-dot forecast-trend-dot" :cx="point.x" :cy="point.y" r="1.6" />
        </svg>
        <div class="trend-labels">
          <span>{{ forecastDays[0]?.dateLabel }}</span>
          <span>{{ forecastDays[forecastDays.length - 1]?.dateLabel }}</span>
        </div>
      </section>
      <section class="forecast-list">
        <article v-for="item in forecastDays" :key="item.date" class="forecast-card">
          <details>
            <summary>
              <div class="forecast-summary">
                <div class="forecast-day">
                  <div><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
                </div>
                <div class="forecast-meta">
                  <span class="forecast-condition">{{ item.condition }}</span>
                  <span class="forecast-temp">{{ item.temp }}</span>
                  <span class="forecast-average">{{ labels.average }} {{ item.averageTempLabel }}</span>
                  <span class="forecast-icon">{{ item.icon }}</span>
                </div>
              </div>
            </summary>
            <div class="forecast-detail-grid">
              <div><p class="detail-label">{{ labels.day }}</p><p>{{ item.dayInfo }}</p></div>
              <div><p class="detail-label">{{ labels.night }}</p><p>{{ item.nightInfo }}</p></div>
            </div>
          </details>
        </article>
      </section>
    </section>
  </section>
</template>

<script setup>
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

const showRangeTrend = computed(() => props.rangeDays.length > 5)
const rangeTrend = computed(() => buildTrendGeometry(props.rangeDays))
const forecastTrend = computed(() => buildTrendGeometry(props.forecastDays))
const rangeTrendPath = computed(() => rangeTrend.value.linePath)
const rangeTrendAreaPath = computed(() => rangeTrend.value.areaPath)
const rangeTrendDots = computed(() => rangeTrend.value.dots)
const forecastTrendPath = computed(() => forecastTrend.value.linePath)
const forecastTrendAreaPath = computed(() => forecastTrend.value.areaPath)
const forecastTrendDots = computed(() => forecastTrend.value.dots)

function buildTrendGeometry(items) {
  const values = items.map((item) => item.averageTempValue).filter((value) => value != null)
  if (!values.length) return { linePath: '', areaPath: '', dots: [] }
  const min = Math.min(...values)
  const max = Math.max(...values)
  const spread = max - min || 1
  const dots = items.map((item, index) => {
    const value = item.averageTempValue ?? min
    const x = items.length === 1 ? 50 : (index / (items.length - 1)) * 100
    const y = 34 - (((value - min) / spread) * 26)
    return { key: `${item.date}-${index}`, x, y }
  })
  const linePath = dots.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ')
  const areaPath = `${linePath} L ${dots[dots.length - 1].x} 40 L ${dots[0].x} 40 Z`
  return { linePath, areaPath, dots }
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
.highlight-card, .range-summary-card, .trend-card { background: #f5faf6; }
.info-header { font-size: 0.9rem; color: #6f8174; margin-bottom: 10px; }
.info-content { display: grid; gap: 8px; }
.current-card { min-height: 100%; }
.current-content { grid-template-columns: auto 1fr; align-items: center; gap: 16px; }
.headline-block { display: grid; gap: 6px; }
.weather-icon { font-size: 3rem; line-height: 1; }
.headline-block strong { font-size: clamp(2rem, 4vw, 3rem); line-height: 1; }
.condition-text { color: #23402e; font-weight: 600; }
.location-text, .region-text { color: #567061; }
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
.trend-card { display: grid; gap: 10px; }
.trend-header { display: flex; justify-content: space-between; gap: 12px; color: #4f6754; }
.trend-chart { width: 100%; height: 140px; display: block; overflow: visible; }
.trend-area { fill: url(#rangeTrendFill); }
.forecast-trend-area { fill: url(#forecastTrendFill); }
.trend-line { fill: none; stroke: #2f7d4b; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
.forecast-trend-line { stroke: #d27b2c; }
.trend-dot { fill: #2f7d4b; stroke: #ffffff; stroke-width: 0.8; }
.forecast-trend-dot { fill: #d27b2c; }
.trend-labels { display: flex; justify-content: space-between; color: #567061; font-size: 0.92rem; }
.forecast-list { display: grid; gap: 12px; }
.forecast-card details { display: grid; gap: 14px; }
.forecast-card summary { list-style: none; cursor: pointer; }
.forecast-card summary::-webkit-details-marker { display: none; }
.forecast-summary { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
.forecast-day { display: grid; grid-template-columns: 1fr; align-items: center; gap: 12px; }
.forecast-icon { font-size: 1.8rem; line-height: 1; align-self: center; }
.forecast-meta { display: grid; gap: 4px; justify-items: end; text-align: right; }
.forecast-condition { color: #4f6754; }
.forecast-temp { font-weight: 700; }
.forecast-average { color: #567061; font-size: 0.92rem; }
.forecast-card p, .detail-label { color: #567061; }
.forecast-detail-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
@media (max-width: 960px) {
  .summary-grid, .range-form, .forecast-detail-grid, .section-heading-row { grid-template-columns: 1fr; }
  .details-grid { grid-template-columns: 1fr; }
  .weather-list-header { flex-direction: column; }
}
</style>
