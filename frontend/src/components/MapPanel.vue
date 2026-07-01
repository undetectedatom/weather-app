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
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: 0 18px 50px rgba(16, 35, 63, 0.08);
  backdrop-filter: blur(14px);
  border-radius: 24px;
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
  color: #5f7392;
}

h2,
p {
  margin: 0;
}

.map {
  min-height: 240px;
  border-radius: 20px;
  background:
    linear-gradient(135deg, rgba(29, 78, 216, 0.14), rgba(56, 189, 248, 0.08)),
    radial-gradient(circle at 22% 28%, rgba(29, 78, 216, 0.26), transparent 18%),
    radial-gradient(circle at 68% 40%, rgba(56, 189, 248, 0.3), transparent 14%),
    radial-gradient(circle at 52% 72%, rgba(29, 78, 216, 0.2), transparent 16%),
    #dbeafe;
  border: 1px solid rgba(29, 78, 216, 0.15);
  position: relative;
  overflow: hidden;
}

.map-overlay {
  position: absolute;
  inset: auto 16px 16px 16px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
  color: #21416f;
  display: grid;
  gap: 4px;
}
</style>
