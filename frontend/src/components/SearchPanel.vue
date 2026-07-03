<template>
  <section class="panel search-panel">
    <div class="section-heading">
      <p class="eyebrow">Search</p>
      <h2>Find weather by location</h2>
    </div>

    <p class="description">
      Enter a city, zip code, landmark, or coordinates. You can later connect this to a real weather lookup.
    </p>

    <form class="search-form" @submit.prevent="submitSearch">
      <input
        v-model="localQuery"
        type="text"
        placeholder="Try: Tokyo, 10001, Golden Gate Bridge"
      />
      <button type="submit" :disabled="loading">{{ loading ? 'Loading...' : 'Submit' }}</button>
    </form>

    <button class="secondary-button" type="button" :disabled="currentLocationLoading" @click="$emit('use-current-location')">
      {{ currentLocationLoading ? 'Locating...' : 'Use my current location' }}
    </button>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <div class="tips">
      <span>City / town</span>
      <span>Zip code</span>
      <span>Coordinates</span>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  query: {
    type: String,
    default: '',
  },
  errorMessage: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  currentLocationLoading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:query', 'search', 'use-current-location'])
const localQuery = ref(props.query)

watch(
  () => props.query,
  (value) => {
    localQuery.value = value
  }
)

watch(localQuery, (value) => {
  emit('update:query', value)
})

function submitSearch() {
  emit('search', localQuery.value)
}
</script>

<style scoped>
.panel {
  background: #ffffff;
  border: 1px solid #cfd8cf;
  border-radius: 18px;
  padding: 22px;
}

.search-panel {
  display: grid;
  gap: 14px;
}

.section-heading {
  display: grid;
  gap: 4px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #6f8174;
}

h2,
p {
  margin: 0;
}

.description {
  color: #567061;
  line-height: 1.6;
}

.search-form {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-form input {
  flex: 1;
  min-width: 0;
  border: 1px solid #cfd8cf;
  border-radius: 12px;
  padding: 12px 14px;
  background: #ffffff;
  color: #17311f;
}

.search-form button,
.secondary-button {
  border: 1px solid #7ab48a;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
}

.search-form button {
  background: #2f7d4b;
  color: white;
}

.secondary-button {
  background: #edf5ef;
  color: #23402e;
}

button:disabled {
  cursor: wait;
  opacity: 0.72;
}

.error-message {
  color: #a63a3a;
  font-size: 0.95rem;
}

.tips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.tips span {
  padding: 8px 12px;
  border-radius: 999px;
  background: #edf5ef;
  border: 1px solid #d6e1d8;
  color: #4f6754;
  font-size: 0.92rem;
}

@media (max-width: 960px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }

  .search-form button,
  .secondary-button {
    width: 100%;
  }
}
</style>
