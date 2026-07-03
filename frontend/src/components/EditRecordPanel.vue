<template>
  <div
    class="overlay-shell"
    @mousedown.self="handleOverlayMouseDown"
    @mouseup.self="handleOverlayMouseUp"
  >
    <section class="edit-panel panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">{{ labels.eyebrow }}</p>
          <h2>{{ labels.title }}</h2>
        </div>
        <button class="icon-button" type="button" @click="$emit('close')">{{ labels.close }}</button>
      </div>
      <form class="edit-form" @submit.prevent="submitEdit">
        <label>
          <span>{{ labels.location }}</span>
          <div class="input-shell">
            <input v-model="localLocation" type="text" @input="handleLocationTyping" />
            <div v-if="locationSuggestions.length" class="suggestions-panel">
              <button
                v-for="item in locationSuggestions"
                :key="`${item.latitude}-${item.longitude}-${item.display_label}`"
                class="suggestion-item"
                type="button"
                @click="chooseSuggestion(item)"
              >
                <strong>{{ item.name }}</strong>
                <span>{{ item.display_label }}</span>
              </button>
            </div>
          </div>
        </label>
        <label>
          <span>{{ labels.startDate }}</span>
          <input v-model="localStartDate" type="date" />
        </label>
        <label>
          <span>{{ labels.endDate }}</span>
          <input v-model="localEndDate" type="date" />
        </label>
        <label>
          <span>{{ labels.notes }}</span>
          <textarea v-model="localNotes" rows="4"></textarea>
        </label>
        <p class="helper-text">{{ labels.helper }}</p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <div class="form-actions">
          <button type="button" class="ghost-button" @click="$emit('close')">{{ labels.cancel }}</button>
          <button type="submit" :disabled="loading">{{ loading ? labels.saving : labels.save }}</button>
        </div>
      </form>
    </section>
  </div>
</template>
<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { apiRequest } from '../api'

const props = defineProps({
  record: { type: Object, required: true },
  labels: { type: Object, required: true },
  loading: { type: Boolean, default: false },
  errorMessage: { type: String, default: '' },
})
const emit = defineEmits(['close', 'save'])
const localLocation = ref(props.record.locationQuery ?? '')
const localStartDate = ref(props.record.startDateRaw ?? '')
const localEndDate = ref(props.record.endDateRaw ?? '')
const localNotes = ref(props.record.notes ?? '')
const selectedLocationQuery = ref(props.record.locationQuery ?? '')
const locationSuggestions = ref([])
const overlayMouseDown = ref(false)
let suggestionTimer = null

watch(() => props.record, (value) => {
  localLocation.value = value.locationQuery ?? ''
  localStartDate.value = value.startDateRaw ?? ''
  localEndDate.value = value.endDateRaw ?? ''
  localNotes.value = value.notes ?? ''
  selectedLocationQuery.value = value.locationQuery ?? ''
  locationSuggestions.value = []
}, { deep: true })

function handleOverlayMouseDown() {
  overlayMouseDown.value = true
}

function handleOverlayMouseUp() {
  if (!overlayMouseDown.value) return
  overlayMouseDown.value = false
  emit('close')
}

function handleLocationTyping() {
  selectedLocationQuery.value = localLocation.value
  if (suggestionTimer) window.clearTimeout(suggestionTimer)
  const trimmed = localLocation.value.trim()
  if (trimmed.length < 2) {
    locationSuggestions.value = []
    return
  }
  suggestionTimer = window.setTimeout(() => {
    fetchSuggestions(trimmed)
  }, 250)
}

async function fetchSuggestions(query) {
  try {
    const payload = await apiRequest(`/locations/search?query=${encodeURIComponent(query)}`)
    locationSuggestions.value = payload.results ?? []
  } catch {
    locationSuggestions.value = []
  }
}

function chooseSuggestion(item) {
  selectedLocationQuery.value = item.name
  localLocation.value = item.display_label
  locationSuggestions.value = []
}

function submitEdit() {
  emit('save', {
    location: selectedLocationQuery.value,
    start_date: localStartDate.value || null,
    end_date: localEndDate.value || null,
    notes: localNotes.value.trim() || null,
  })
}

onBeforeUnmount(() => {
  if (suggestionTimer) window.clearTimeout(suggestionTimer)
})
</script>
<style scoped>
.overlay-shell { position: fixed; inset: 0; background: rgba(23,49,31,0.24); display: flex; justify-content: center; align-items: center; z-index: 70; padding: 18px; }
.panel { width: min(520px, 100%); background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.panel-header { display: flex; justify-content: space-between; gap: 12px; align-items: center; margin-bottom: 18px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.edit-form { display: grid; gap: 14px; }
.edit-form label { display: grid; gap: 6px; color: #4f6754; }
.input-shell { position: relative; }
.edit-form input, .edit-form textarea { border: 1px solid #cfd8cf; border-radius: 12px; padding: 12px 14px; background: white; font: inherit; }
.suggestions-panel { position: absolute; top: calc(100% + 8px); left: 0; right: 0; z-index: 3; border: 1px solid #cfd8cf; border-radius: 14px; background: #ffffff; padding: 10px; display: grid; gap: 8px; }
.suggestion-item { border: 1px solid #dbe4dc; border-radius: 12px; background: #f7faf7; color: #17311f; text-align: left; padding: 10px 12px; display: grid; gap: 2px; cursor: pointer; }
.helper-text { color: #4f6754; background: #f7faf7; border: 1px solid #dbe4dc; border-radius: 12px; padding: 12px; }
.error-message { color: #a63a3a; background: #fff4f4; border: 1px solid #e4bbbb; border-radius: 12px; padding: 12px; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; }
.form-actions button, .icon-button, .ghost-button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 10px 14px; cursor: pointer; background: #ffffff; color: #23402e; }
.form-actions button[type="submit"] { background: #2f7d4b; border-color: #7ab48a; color: white; }
</style>
