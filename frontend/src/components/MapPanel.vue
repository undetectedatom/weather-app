<template>
  <aside class="panel map-panel">
    <div class="section-heading">
      <p class="eyebrow">{{ labels.eyebrow }}</p>
      <h2>{{ labels.title }}</h2>
      <p class="location-heading">{{ locationLabel }}</p>
    </div>

    <div class="map">
      <iframe v-if="latitude != null && longitude != null" class="map-frame" :src="embedUrl" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <div class="map-overlay">
        <p class="overlay-title">{{ locationLabel }}</p>
        <span v-if="regionLabel">{{ regionLabel }}</span>
        <strong v-if="latitude != null && longitude != null">{{ latitude.toFixed(3) }}, {{ longitude.toFixed(3) }}</strong>
        <a v-if="latitude != null && longitude != null" class="map-link" :href="mapLink" target="_blank" rel="noreferrer">{{ labels.openStreetMap }}</a>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  locationLabel: { type: String, required: true },
  regionLabel: { type: String, default: '' },
  latitude: { type: Number, default: null },
  longitude: { type: Number, default: null },
  labels: { type: Object, required: true },
})

const embedUrl = computed(() => {
  if (props.latitude == null || props.longitude == null) return ''
  const delta = 0.08
  const left = props.longitude - delta
  const right = props.longitude + delta
  const top = props.latitude + delta
  const bottom = props.latitude - delta
  return `https://www.openstreetmap.org/export/embed.html?bbox=${left}%2C${bottom}%2C${right}%2C${top}&layer=mapnik&marker=${props.latitude}%2C${props.longitude}`
})
const mapLink = computed(() => props.latitude == null || props.longitude == null ? '#' : `https://www.openstreetmap.org/?mlat=${props.latitude}&mlon=${props.longitude}#map=11/${props.latitude}/${props.longitude}`)
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.map-panel { display: grid; gap: 14px; }
.section-heading { display: grid; gap: 4px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.location-heading { color: #23402e; font-size: 1rem; font-weight: 600; }
.map { min-height: 240px; border-radius: 14px; background: #f3f7f3; border: 1px solid #cfd8cf; position: relative; overflow: hidden; }
.map-frame { width: 100%; height: 100%; min-height: 240px; border: 0; }
.map-overlay { position: absolute; inset: auto 16px 16px 16px; padding: 14px; border-radius: 12px; background: rgba(255,255,255,0.94); border: 1px solid #cfd8cf; color: #23402e; display: grid; gap: 4px; }
.overlay-title { font-weight: 700; }
.map-link { color: #2f7d4b; text-decoration: none; font-weight: 600; }
</style>
