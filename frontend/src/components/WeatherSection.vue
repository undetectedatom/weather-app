<template>
  <section class="panel weather-panel">
    <div class="section-heading section-heading-row">
      <div>
        <p class="eyebrow">Weather</p>
        <h2>Current conditions</h2>
      </div>

      <nav class="time-selection" aria-label="Weather range">
        <button
          type="button"
          :class="{ active: activeView === 'now' }"
          @click="$emit('change-view', 'now')"
        >
          Now
        </button>
        <button
          type="button"
          :class="{ active: activeView === 'forecast' }"
          @click="$emit('change-view', 'forecast')"
        >
          5 Day
        </button>
        <button
          type="button"
          :class="{ active: activeView === 'customRange' }"
          @click="$emit('change-view', 'customRange')"
        >
          Custom range
        </button>
      </nav>
    </div>

    <div v-if="activeView === 'now'" class="summary-grid">
      <article class="info-card highlight-card">
        <div class="info-header">Location</div>
        <div class="info-content">
          <strong>{{ selectedLocation }}</strong>
          <p>{{ currentWeather.region }}</p>
        </div>
      </article>

      <article class="info-card">
        <div class="info-header">Current weather</div>
        <div class="info-content">
          <div class="weather-icon">{{ currentWeather.icon }}</div>
          <strong>{{ currentWeather.temperature }}</strong>
          <p>{{ currentWeather.condition }}</p>
        </div>
      </article>

      <article class="info-card">
        <div class="info-header">Useful details</div>
        <div class="info-content details-list">
          <p>{{ currentWeather.feelsLike }}</p>
          <p>{{ currentWeather.humidity }}</p>
          <p>{{ currentWeather.wind }}</p>
        </div>
      </article>
    </div>

    <section v-else-if="activeView === 'customRange'" class="custom-range-card">
      <div class="section-heading">
        <p class="eyebrow">Custom range</p>
        <h2>Choose a date range</h2>
      </div>

      <form class="range-form" @submit.prevent="submitRange">
        <label>
          <span>Start date</span>
          <input v-model="startDate" type="date" />
        </label>
        <label>
          <span>End date</span>
          <input v-model="endDate" type="date" />
        </label>
        <button type="submit">Check range</button>
      </form>
    </section>

    <section v-else class="forecast-list">
      <article v-for="item in forecastDays" :key="item.day" class="forecast-card">
        <details>
          <summary>
            <div class="forecast-summary">
              <div>
                <strong>{{ item.day }}</strong>
                <p>{{ item.date }}</p>
              </div>
              <div class="forecast-meta">
                <span class="forecast-condition">{{ item.condition }}</span>
                <span class="forecast-temp">{{ item.temp }}</span>
              </div>
            </div>
          </summary>
          <div class="forecast-detail-grid">
            <div>
              <p class="detail-label">Day</p>
              <p>{{ item.dayInfo }}</p>
            </div>
            <div>
              <p class="detail-label">Night</p>
              <p>{{ item.nightInfo }}</p>
            </div>
          </div>
        </details>
      </article>
    </section>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  activeView: {
    type: String,
    required: true,
  },
  selectedLocation: {
    type: String,
    required: true,
  },
  currentWeather: {
    type: Object,
    required: true,
  },
  forecastDays: {
    type: Array,
    required: true,
  },
  customRange: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['change-view', 'submit-range'])
const startDate = ref(props.customRange.startDate)
const endDate = ref(props.customRange.endDate)

watch(
  () => props.customRange.startDate,
  (value) => {
    startDate.value = value
  }
)

watch(
  () => props.customRange.endDate,
  (value) => {
    endDate.value = value
  }
)

function submitRange() {
  emit('submit-range', {
    startDate: startDate.value,
    endDate: endDate.value,
  })
}
</script>

<style scoped>
.panel {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: 0 18px 50px rgba(16, 35, 63, 0.08);
  backdrop-filter: blur(14px);
  border-radius: 24px;
  padding: 22px;
}

.weather-panel {
  display: grid;
  gap: 18px;
}

.section-heading {
  display: grid;
  gap: 4px;
}

.section-heading-row {
  grid-template-columns: 1fr auto;
  align-items: center;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #5f7392;
}

h2,
p {
  margin: 0;
}

.time-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.time-selection button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
  background: #eef4ff;
  color: #21416f;
}

.time-selection .active {
  background: #1d4ed8;
  color: white;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.info-card,
.forecast-card,
.custom-range-card {
  border-radius: 18px;
  border: 1px solid rgba(16, 35, 63, 0.08);
  background: white;
  padding: 16px;
}

.highlight-card {
  background: linear-gradient(160deg, #eff6ff, #ffffff);
}

.info-header {
  font-size: 0.9rem;
  color: #57708f;
  margin-bottom: 10px;
}

.info-content {
  display: grid;
  gap: 8px;
}

.weather-icon {
  font-size: 2rem;
}

.details-list p {
  color: #21416f;
}

.custom-range-card {
  display: grid;
  gap: 14px;
}

.range-form {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  align-items: end;
}

.range-form label {
  display: grid;
  gap: 6px;
  color: #4f6786;
  font-size: 0.92rem;
}

.range-form input {
  border: 1px solid rgba(16, 35, 63, 0.12);
  border-radius: 14px;
  padding: 12px 14px;
  background: white;
}

.range-form button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

.forecast-list {
  display: grid;
  gap: 10px;
}

.forecast-card details {
  width: 100%;
}

.forecast-card summary {
  list-style: none;
  cursor: pointer;
}

.forecast-card summary::-webkit-details-marker {
  display: none;
}

.forecast-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.forecast-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: right;
}

.forecast-condition {
  color: #57708f;
}

.forecast-temp {
  font-size: 1.1rem;
  font-weight: 700;
  color: #10233f;
}

.forecast-card p,
.detail-label {
  color: #57708f;
}

.forecast-detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(16, 35, 63, 0.08);
}

.detail-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
}

@media (max-width: 960px) {
  .section-heading-row,
  .summary-grid,
  .range-form,
  .forecast-detail-grid {
    grid-template-columns: 1fr;
  }

  .forecast-summary {
    flex-direction: column;
    align-items: flex-start;
  }

  .forecast-meta {
    text-align: left;
  }
}
</style>
