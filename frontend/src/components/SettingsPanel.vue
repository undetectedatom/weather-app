<template>
  <div class="overlay-shell" @click.self="$emit('close')">
    <section class="settings-panel panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">{{ labels.eyebrow }}</p>
          <h2>{{ labels.title }}</h2>
        </div>
        <button class="icon-button" type="button" @click="$emit('close')">{{ labels.close }}</button>
      </div>
      <form class="settings-form" @submit.prevent="saveSettings">
        <label>
          <span>{{ labels.language }}</span>
          <select v-model="localLanguage">
            <option>English</option>
            <option>Spanish</option>
            <option>French</option>
            <option>Chinese</option>
          </select>
        </label>
        <label>
          <span>{{ labels.temperature }}</span>
          <select v-model="localTemperatureUnit">
            <option value="C">{{ labels.celsius }}</option>
            <option value="F">{{ labels.fahrenheit }}</option>
          </select>
        </label>
        <button type="submit">{{ labels.save }}</button>
      </form>
    </section>
  </div>
</template>
<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ language: { type: String, required: true }, temperatureUnit: { type: String, required: true }, labels: { type: Object, required: true } })
const emit = defineEmits(['close', 'save'])
const localLanguage = ref(props.language)
const localTemperatureUnit = ref(props.temperatureUnit)
watch(() => props.language, (value) => { localLanguage.value = value })
watch(() => props.temperatureUnit, (value) => { localTemperatureUnit.value = value })
function saveSettings() { emit('save', { language: localLanguage.value, temperatureUnit: localTemperatureUnit.value }) }
</script>
<style scoped>
.overlay-shell { position: fixed; inset: 0; background: rgba(23, 49, 31, 0.24); display: flex; justify-content: flex-end; z-index: 50; }
.panel { width: min(360px, 100%); background: #ffffff; border-left: 1px solid #cfd8cf; padding: 22px; }
.panel-header { display: flex; justify-content: space-between; gap: 12px; align-items: center; margin-bottom: 18px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.settings-form { display: grid; gap: 14px; }
.settings-form label { display: grid; gap: 6px; color: #4f6754; }
.settings-form select { border: 1px solid #cfd8cf; border-radius: 12px; padding: 12px 14px; background: white; }
.settings-form button, .icon-button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 10px 14px; cursor: pointer; }
.settings-form button { background: #2f7d4b; color: white; border-color: #7ab48a; }
.icon-button { background: #ffffff; color: #23402e; }
@media (max-width: 640px) { .overlay-shell { justify-content: stretch; } .panel { width: 100%; min-height: 100%; border-left: 0; } }
</style>
