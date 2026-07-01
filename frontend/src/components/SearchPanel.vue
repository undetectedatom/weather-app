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
      <button type="submit">Submit</button>
    </form>

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
})

const emit = defineEmits(['update:query', 'search'])
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
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: 0 18px 50px rgba(16, 35, 63, 0.08);
  backdrop-filter: blur(14px);
  border-radius: 24px;
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
  color: #5f7392;
}

h2,
p {
  margin: 0;
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

.search-form input {
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(16, 35, 63, 0.12);
  border-radius: 14px;
  padding: 12px 14px;
  background: white;
}

.search-form button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

.error-message {
  color: #b91c1c;
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
  background: rgba(16, 35, 63, 0.05);
  color: #4f6786;
  font-size: 0.92rem;
}

@media (max-width: 960px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }

  .search-form button {
    width: 100%;
  }
}
</style>
