<template>
  <div class="overlay-shell" @click.self="$emit('close')">
    <section class="settings-panel panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">Settings</p>
          <h2>Display options</h2>
        </div>
        <button class="icon-button" type="button" @click="$emit('close')">Close</button>
      </div>

      <form class="settings-form" @submit.prevent="saveSettings">
        <label>
          <span>Language</span>
          <select v-model="localLanguage">
            <option>English</option>
            <option>Spanish</option>
            <option>French</option>
            <option>Chinese</option>
          </select>
        </label>

        <label>
          <span>Temperature</span>
          <select v-model="localTemperatureUnit">
            <option value="C">Celsius</option>
            <option value="F">Fahrenheit</option>
          </select>
        </label>

        <button type="submit">Save settings</button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  language: {
    type: String,
    required: true,
  },
  temperatureUnit: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['close', 'save'])
const localLanguage = ref(props.language)
const localTemperatureUnit = ref(props.temperatureUnit)

watch(
  () => props.language,
  (value) => {
    localLanguage.value = value
  }
)

watch(
  () => props.temperatureUnit,
  (value) => {
    localTemperatureUnit.value = value
  }
)

function saveSettings() {
  emit('save', {
    language: localLanguage.value,
    temperatureUnit: localTemperatureUnit.value,
  })
}
</script>

<style scoped>
.overlay-shell {
  position: fixed;
  inset: 0;
  background: rgba(8, 15, 28, 0.32);
  display: flex;
  justify-content: flex-end;
  z-index: 50;
}

.panel {
  width: min(360px, 100%);
  background: rgba(255, 255, 255, 0.96);
  border-left: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: -18px 0 50px rgba(16, 35, 63, 0.14);
  padding: 22px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 18px;
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

.settings-form {
  display: grid;
  gap: 14px;
}

.settings-form label {
  display: grid;
  gap: 6px;
  color: #4f6786;
}

.settings-form select {
  border: 1px solid rgba(16, 35, 63, 0.12);
  border-radius: 14px;
  padding: 12px 14px;
  background: white;
}

.settings-form button,
.icon-button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
}

.settings-form button {
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

.icon-button {
  background: #eef4ff;
  color: #21416f;
}

@media (max-width: 640px) {
  .overlay-shell {
    justify-content: stretch;
  }

  .panel {
    width: 100%;
    min-height: 100%;
    border-left: 0;
  }
}
</style>
