<template>
  <header class="header panel">
    <div class="brand">
      <img class="brand-mark" :src="brandLogo" alt="HelloWeather logo" />
      <div>
        <p class="eyebrow">{{ labels.eyebrow }}</p>
        <h1>HelloWeather</h1>
      </div>
    </div>
    <div class="header-right">
      <button class="ghost-button" type="button">{{ selectedLocation }}</button>
      <button class="ghost-button" type="button">{{ temperatureUnit }}°</button>
      <button class="primary-button" type="button" @click="$emit('home')">{{ labels.home }}</button>
      <button class="primary-button" type="button" @click="$emit('open-dashboard')">{{ labels.dashboard }}</button>
      <button class="primary-button" type="button" @click="$emit('open-settings')">{{ labels.settings }}</button>
      <button v-if="!isAuthenticated" class="primary-button" type="button" @click="$emit('open-auth')">{{ labels.signIn }}</button>
      <button v-else class="ghost-button" type="button">{{ userEmail || labels.signedInFallback }}</button>
      <button v-if="isAuthenticated" class="ghost-button" type="button" @click="$emit('request-logout')">{{ labels.signOut }}</button>
    </div>
  </header>
</template>

<script setup>
import brandLogo from '../assets/brand/logo.png'

defineProps({
  selectedLocation: { type: String, required: true },
  temperatureUnit: { type: String, required: true },
  isAuthenticated: { type: Boolean, default: false },
  userEmail: { type: String, default: '' },
  labels: { type: Object, required: true },
})
defineEmits(['open-settings', 'open-auth', 'open-dashboard', 'home', 'request-logout'])
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; }
.header { display: flex; align-items: center; justify-content: space-between; gap: 16px; border-radius: 18px; padding: 18px 20px; }
.brand { display: flex; align-items: center; gap: 14px; }
.brand-mark { width: 44px; height: 44px; border-radius: 12px; object-fit: cover; flex: 0 0 auto; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h1, p { margin: 0; }
h1 { font-size: 1.4rem; }
.header-right { margin-left: auto; display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-end; align-items: center; }
.ghost-button, .primary-button { border-radius: 12px; padding: 10px 14px; cursor: pointer; border: 1px solid #cfd8cf; background: #ffffff; color: #23402e; max-width: 150px; min-height: 42px; }
.primary-button { border-color: #7ab48a; background: #2f7d4b; color: white; }
@media (max-width: 640px) {
  .header { align-items: start; }
  .header-right { gap: 8px; }
  .ghost-button, .primary-button { max-width: none; }
}
@media (max-width: 430px) {
  .header { flex-direction: column; align-items: stretch; gap: 14px; padding: 16px; }
  .brand { flex: 1 1 auto; }
  .header-right {
    margin-left: 0;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    justify-content: stretch;
  }
  .header-right button {
    width: 100%;
    max-width: none;
    padding: 9px 12px;
  }
}
</style>
