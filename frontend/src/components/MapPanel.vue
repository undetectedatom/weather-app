<template>
  <aside class="panel map-panel">
    <div class="section-heading">
      <p class="eyebrow">Map preview</p>
      <h2>Location area</h2>
    </div>

    <div class="map">
      <div class="map-overlay">
        <p>{{ locationLabel }}</p>
        <span>{{ regionLabel || 'Resolved location details will appear here.' }}</span>
        <strong v-if="latitude != null && longitude != null">{{ latitude.toFixed(3) }}, {{ longitude.toFixed(3) }}</strong>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  locationLabel: {
    type: String,
    required: true,
  },
  regionLabel: {
    type: String,
    default: '',
  },
  latitude: {
    type: Number,
    default: null,
  },
  longitude: {
    type: Number,
    default: null,
  },
})
</script>

<style scoped>
.panel {
  background: #ffffff;
  border: 1px solid #cfd8cf;
  border-radius: 18px;
  padding: 22px;
}

.map-panel {
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

.map {
  min-height: 240px;
  border-radius: 14px;
  background:
    radial-gradient(circle at top left, rgba(122, 180, 138, 0.26), transparent 34%),
    linear-gradient(135deg, #f3f7f3 0%, #e6f0e8 100%);
  border: 1px solid #cfd8cf;
  position: relative;
  overflow: hidden;
}

.map-overlay {
  position: absolute;
  inset: auto 16px 16px 16px;
  padding: 14px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #cfd8cf;
  color: #23402e;
  display: grid;
  gap: 4px;
}
</style>
