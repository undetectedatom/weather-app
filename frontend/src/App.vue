<script setup>
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
</script>

<template>
  <div class="page-shell">
    <header class="header">
      <div class="brand">
        <div class="brand-mark">HW</div>
        <div>
          <p class="eyebrow">Weather demo</p>
          <h1>HelloWeather</h1>
        </div>
      </div>

      <div class="header-middle">
        <span class="status-pill">Enter a location to see details</span>
      </div>

      <div class="header-right">
        <button class="ghost-button" type="button">Settings</button>
        <button class="primary-button" type="button">Sign In</button>
      </div>
    </header>

    <main class="top-grid">
      <section class="panel search-panel">
        <div class="section-heading">
          <p class="eyebrow">Search</p>
          <h2>Find weather by location</h2>
        </div>

        <p class="description">
          Enter a city, zip code, landmark, or coordinates. You can later connect this to a real weather lookup.
        </p>

        <form class="search-form" action="">
          <input type="text" placeholder="Try: Tokyo, 10001, Golden Gate Bridge" />
          <button type="button">Submit</button>
        </form>

        <div class="tips">
          <span>City / town</span>
          <span>Zip code</span>
          <span>Coordinates</span>
        </div>
      </section>

      <aside class="panel map-panel">
        <div class="section-heading">
          <p class="eyebrow">Map preview</p>
          <h2>Location area</h2>
        </div>

        <div class="map">
          <div class="map-overlay">
            <p>Map placeholder</p>
            <span>Later this can show an approximate point of interest or resolved location.</span>
          </div>
        </div>
      </aside>
    </main>

    <section class="panel weather-panel">
      <div class="section-heading section-heading-row">
        <div>
          <p class="eyebrow">Weather</p>
          <h2>Current conditions</h2>
        </div>
        <nav class="time-selection" aria-label="Weather range">
          <button class="active" type="button">Now</button>
          <button type="button">5 Day</button>
          <button type="button">Custom range</button>
        </nav>
      </div>

      <div class="summary-grid">
        <article class="info-card highlight-card">
          <div class="info-header">Location</div>
          <div class="info-content">
            <strong>San Francisco</strong>
            <p>California, United States</p>
          </div>
        </article>

        <article class="info-card">
          <div class="info-header">Current weather</div>
          <div class="info-content">
            <div class="weather-icon">☀️</div>
            <strong>24°C</strong>
            <p>Clear sky</p>
          </div>
        </article>

        <article class="info-card">
          <div class="info-header">Useful details</div>
          <div class="info-content details-list">
            <p>Feels like 23°C</p>
            <p>Humidity 61%</p>
            <p>Wind 8 km/h</p>
          </div>
        </article>
      </div>

      <section class="custom-range-card">
        <div class="section-heading">
          <p class="eyebrow">Custom range</p>
          <h2>Choose a date range</h2>
        </div>

        <form class="range-form" action="">
          <label>
            <span>Start date</span>
            <input type="date" />
          </label>
          <label>
            <span>End date</span>
            <input type="date" />
          </label>
          <button type="button">Check range</button>
        </form>
      </section>

      <section class="forecast-list">
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

.header,
.panel {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: 0 18px 50px rgba(16, 35, 63, 0.08);
  backdrop-filter: blur(14px);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-radius: 24px;
  padding: 18px 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #5f7392;
}

h1,
h2,
p {
  margin: 0;
}

h1 {
  font-size: 1.4rem;
}

h2 {
  font-size: 1.15rem;
}

.header-middle {
  flex: 1;
  display: flex;
  justify-content: center;
}

.status-pill {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(29, 78, 216, 0.08);
  color: #1d4ed8;
  font-size: 0.95rem;
}

.header-right {
  display: flex;
  gap: 10px;
}

.ghost-button,
.primary-button,
.search-form button,
.time-selection button,
.range-form button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
}

.ghost-button,
.time-selection button {
  background: #eef4ff;
  color: #21416f;
}

.primary-button,
.search-form button,
.range-form button {
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

.top-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
  gap: 20px;
}

.panel {
  border-radius: 24px;
  padding: 22px;
}

.search-panel {
  display: grid;
  gap: 14px;
}

.description {
  color: #57708f;
  line-height: 1.6;
}

.search-form {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-form input,
.range-form input {
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(16, 35, 63, 0.12);
  border-radius: 14px;
  padding: 12px 14px;
  background: white;
}

.tips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tips span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(16, 35, 63, 0.05);
  color: #4f6786;
  font-size: 0.92rem;
}

.map {
  min-height: 240px;
  border-radius: 20px;
  background:
    linear-gradient(135deg, rgba(29, 78, 216, 0.14), rgba(56, 189, 248, 0.08)),
    radial-gradient(circle at 22% 28%, rgba(29, 78, 216, 0.26), transparent 18%),
    radial-gradient(circle at 68% 40%, rgba(56, 189, 248, 0.3), transparent 14%),
    radial-gradient(circle at 52% 72%, rgba(29, 78, 216, 0.2), transparent 16%),
    #dbeafe;
  border: 1px solid rgba(29, 78, 216, 0.15);
  position: relative;
  overflow: hidden;
}

.map-overlay {
  position: absolute;
  inset: auto 16px 16px 16px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
  color: #21416f;
  display: grid;
  gap: 4px;
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

.time-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
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
  .top-grid,
  .summary-grid,
  .range-form,
  .forecast-detail-grid {
    grid-template-columns: 1fr;
  }

  .header,
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }

  .header-middle {
    justify-content: flex-start;
  }

  .header-right button,
  .search-form button,
  .range-form button {
    width: 100%;
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
