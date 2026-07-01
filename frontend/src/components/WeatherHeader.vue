<template>
  <header class="header panel">
    <div class="brand">
      <div class="brand-mark">HW</div>
      <div>
        <p class="eyebrow">Weather demo</p>
        <h1>HelloWeather</h1>
      </div>
    </div>

    <div class="header-middle">
      <span class="status-pill">{{ statusText }}</span>
    </div>

    <div class="header-right">
      <button class="ghost-button" type="button">{{ selectedLocation }}</button>
      <button class="primary-button" type="button">Settings</button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  selectedLocation: {
    type: String,
    required: true,
  },
  statusText: {
    type: String,
    required: true,
  },
})
</script>

<style scoped>
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
p {
  margin: 0;
}

h1 {
  font-size: 1.4rem;
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
.primary-button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
}

.ghost-button {
  background: #eef4ff;
  color: #21416f;
}

.primary-button {
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

@media (max-width: 960px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-middle {
    justify-content: flex-start;
  }

  .header-right button {
    width: 100%;
  }
}
</style>
