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
      <button class="ghost-button" type="button">{{ temperatureUnit }}°</button>
      <button class="primary-button" type="button" @click="$emit('open-settings')">Settings</button>
      <button class="primary-button" type="button" @click="$emit('open-auth')">Sign In</button>
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
  temperatureUnit: {
    type: String,
    required: true,
  },
})

defineEmits(['open-settings', 'open-auth'])
</script>

<style scoped>
.panel {
  background: #ffffff;
  border: 1px solid #cfd8cf;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-radius: 18px;
  padding: 18px 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: #e8f3ea;
  border: 1px solid #b9d0bc;
  color: #2f7d4b;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #6f8174;
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
  padding: 8px 12px;
  border-radius: 999px;
  background: #edf5ef;
  border: 1px solid #d6e1d8;
  color: #2f7d4b;
  font-size: 0.95rem;
}

.header-right {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
}

.ghost-button,
.primary-button {
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  border: 1px solid #cfd8cf;
  background: #ffffff;
  color: #23402e;
}

.primary-button {
  border-color: #7ab48a;
  background: #2f7d4b;
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
