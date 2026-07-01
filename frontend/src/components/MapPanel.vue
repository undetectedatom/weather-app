<template>
  <aside class="panel map-panel">
    <div class="section-heading">
      <p class="eyebrow">Map preview</p>
      <h2>Location area</h2>
    </div>

    <div class="map">
      <div class="map-overlay">
        <p>{{ locationLabel }}</p>
        <span>Later this can show an approximate point of interest or resolved location.</span>
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
  background: #f3f7f3;
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
