<template>
  <section class="panel search-panel">
    <div class="section-heading">
      <p class="eyebrow">{{ labels.eyebrow }}</p>
      <h2>{{ labels.title }}</h2>
    </div>

    <p class="description">{{ labels.description }}</p>

    <form class="search-form" @submit.prevent="submitSearch">
      <div class="input-shell">
        <input
          v-model="localQuery"
          type="text"
          :placeholder="labels.placeholder"
          @input="emit('typing', localQuery)"
        />
        <div v-if="suggestions.length" class="suggestions-panel">
          <div class="suggestions-title">{{ labels.suggestions }}</div>
          <button
            v-for="item in suggestions"
            :key="`${item.latitude}-${item.longitude}-${item.display_label}`"
            class="suggestion-item"
            type="button"
            @click="$emit('select-suggestion', item)"
          >
            <strong>{{ item.name }}</strong>
            <span>{{ item.display_label }}</span>
          </button>
        </div>
      </div>
      <button type="submit" :disabled="loading">{{ loading ? labels.loading : labels.submit }}</button>
    </form>

    <button class="secondary-button" type="button" :disabled="currentLocationLoading" @click="$emit('use-current-location')">
      {{ currentLocationLoading ? labels.currentLocationLoading : labels.currentLocation }}
    </button>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  query: { type: String, default: '' },
  errorMessage: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  currentLocationLoading: { type: Boolean, default: false },
  suggestions: { type: Array, default: () => [] },
  labels: { type: Object, required: true },
})

const emit = defineEmits(['update:query', 'search', 'use-current-location', 'select-suggestion', 'typing'])
const localQuery = ref(props.query)

watch(() => props.query, (value) => { localQuery.value = value })
watch(localQuery, (value) => { emit('update:query', value) })

function submitSearch() { emit('search', localQuery.value) }
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.search-panel { display: grid; gap: 14px; }
.section-heading { display: grid; gap: 4px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.description { color: #567061; line-height: 1.6; }
.search-form { display: flex; gap: 12px; align-items: flex-start; }
.input-shell { flex: 1; min-width: 0; position: relative; }
.search-form input { width: 100%; border: 1px solid #cfd8cf; border-radius: 12px; padding: 12px 14px; background: #ffffff; color: #17311f; }
.suggestions-panel { position: absolute; top: calc(100% + 8px); left: 0; right: 0; z-index: 5; border: 1px solid #cfd8cf; border-radius: 14px; background: #ffffff; padding: 10px; display: grid; gap: 8px; }
.suggestions-title { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.12em; color: #6f8174; }
.suggestion-item { border: 1px solid #dbe4dc; border-radius: 12px; background: #f7faf7; color: #17311f; text-align: left; padding: 10px 12px; display: grid; gap: 2px; cursor: pointer; }
.search-form button, .secondary-button { border: 1px solid #7ab48a; border-radius: 12px; padding: 10px 14px; cursor: pointer; }
.search-form button { background: #2f7d4b; color: white; }
.secondary-button { background: #edf5ef; color: #23402e; width: fit-content; max-width: min(100%, 20rem); align-self: start; white-space: nowrap; }
button:disabled { cursor: wait; opacity: 0.72; }
.error-message { color: #a63a3a; font-size: 0.95rem; }
@media (max-width: 960px) {
  .secondary-button { width: fit-content; }
}
@media (max-width: 720px) {
  .search-form { flex-direction: column; align-items: stretch; }
  .search-form button { width: 100%; }
  .secondary-button { width: auto; max-width: 100%; }
}
</style>
