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
      <article class="info-card highlight-card">
        <div class="info-header">{{ labels.location }}</div>
        <div class="info-content"><strong>{{ selectedLocation }}</strong><p>{{ currentWeather.region }}</p></div>
      </article>
      <article class="info-card">
        <div class="info-header">{{ labels.currentWeather }}</div>
        <div class="info-content"><div class="weather-icon">{{ currentWeather.icon }}</div><strong>{{ currentTemperature }}</strong><p>{{ currentWeather.condition }}</p></div>
      </article>
      <article class="info-card">
        <div class="info-header">{{ labels.usefulDetails }}</div>
        <div class="info-content details-list"><p>{{ feelsLikeText }}</p><p>{{ currentWeather.humidity }}</p><p>{{ currentWeather.wind }}</p></div>
      </article>
    </div>

    <section v-else-if="activeView === 'customRange'" class="custom-range-card">
      <div class="section-heading"><p class="eyebrow">{{ labels.customEyebrow }}</p><h2>{{ labels.customTitle }}</h2></div>
      <form class="range-form" @submit.prevent="submitRange">
        <label><span>{{ labels.startDate }}</span><input v-model="startDate" type="date" :disabled="rangeLoading" /></label>
        <label><span>{{ labels.endDate }}</span><input v-model="endDate" type="date" :disabled="rangeLoading" /></label>
        <button type="submit" :disabled="rangeLoading">{{ rangeLoading ? labels.checkingRange : labels.checkRange }}</button>
      </form>
      <div v-if="rangeSummary" class="range-summary-card">
        <strong>{{ rangeSummary.start_date }} to {{ rangeSummary.end_date }}</strong>
        <p>{{ labels.average }} {{ rangeSummary.averageTemp }}</p>
        <p>{{ labels.highLow }} {{ rangeSummary.maxTemp }} / Low {{ rangeSummary.minTemp }}</p>
      </div>
      <section v-if="rangeDays.length" class="forecast-list">
        <article v-for="item in rangeDays" :key="item.date" class="forecast-card">
          <details>
            <summary>
              <div class="forecast-summary">
                <div><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
                <div class="forecast-meta"><span class="forecast-condition">{{ item.condition }}</span><span class="forecast-temp">{{ item.temp }}</span></div>
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

    <section v-else class="forecast-list">
      <article v-for="item in forecastDays" :key="item.date" class="forecast-card">
        <details>
          <summary>
            <div class="forecast-summary">
              <div><strong>{{ item.day }}</strong><p>{{ item.dateLabel }}</p></div>
              <div class="forecast-meta"><span class="forecast-condition">{{ item.condition }}</span><span class="forecast-temp">{{ item.temp }}</span></div>
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
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ activeView: { type: String, required: true }, selectedLocation: { type: String, required: true }, currentWeather: { type: Object, required: true }, forecastDays: { type: Array, required: true }, customRange: { type: Object, required: true }, rangeDays: { type: Array, default: () => [] }, rangeSummary: { type: Object, default: null }, currentTemperature: { type: String, required: true }, feelsLikeText: { type: String, required: true }, errorMessage: { type: String, default: '' }, labels: { type: Object, required: true }, rangeLoading: { type: Boolean, default: false } })
const emit = defineEmits(['change-view', 'submit-range'])
const startDate = ref(props.customRange.startDate)
const endDate = ref(props.customRange.endDate)
watch(() => props.customRange.startDate, (value) => { startDate.value = value })
watch(() => props.customRange.endDate, (value) => { endDate.value = value })
function submitRange() { emit('submit-range', { startDate: startDate.value, endDate: endDate.value }) }
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.weather-panel { display: grid; gap: 18px; }
.section-heading { display: grid; gap: 4px; }
.section-heading-row { grid-template-columns: 1fr auto; align-items: center; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.error-banner { border: 1px solid #e4bbbb; border-radius: 12px; padding: 12px 14px; background: #fff4f4; color: #a63a3a; }
.time-selection { display: flex; flex-wrap: wrap; gap: 8px; }
.time-selection button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 10px 14px; cursor: pointer; background: #ffffff; color: #23402e; }
.time-selection .active { background: #edf5ef; border-color: #7ab48a; color: #2f7d4b; }
.summary-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.info-card, .forecast-card, .custom-range-card, .range-summary-card { border-radius: 14px; border: 1px solid #cfd8cf; background: white; padding: 16px; }
.highlight-card { background: #f5faf6; }
.info-header { font-size: 0.9rem; color: #6f8174; margin-bottom: 10px; }
.info-content { display: grid; gap: 8px; }
.weather-icon { font-size: 2rem; }
.details-list p { color: #23402e; }
.custom-range-card { display: grid; gap: 14px; }
.range-summary-card { background: #f5faf6; display: grid; gap: 6px; }
.range-form { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; align-items: end; }
.range-form label { display: grid; gap: 6px; }
.range-form input, .range-form button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 12px 14px; }
.range-form button { cursor: pointer; background: #2f7d4b; border-color: #7ab48a; color: #fff; }
.range-form button:disabled, .range-form input:disabled { cursor: wait; opacity: 0.72; }
.forecast-list { display: grid; gap: 12px; }
.forecast-card details { display: grid; gap: 14px; }
.forecast-card summary { list-style: none; cursor: pointer; }
.forecast-card summary::-webkit-details-marker { display: none; }
.forecast-summary { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
.forecast-meta { display: grid; gap: 4px; justify-items: end; }
.forecast-condition { color: #4f6754; }
.forecast-temp { font-weight: 700; }
.forecast-card p, .detail-label { color: #567061; }
.forecast-detail-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
@media (max-width: 960px) {
  .summary-grid, .range-form, .forecast-detail-grid, .section-heading-row { grid-template-columns: 1fr; }
}
</style>
