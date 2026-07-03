<template>
  <header class="header panel">
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">HW</div>
      <div>
        <p class="eyebrow">{{ labels.eyebrow }}</p>
        <h1>HelloWeather</h1>
      </div>
    </div>
    <div class="header-right">
      <button class="ghost-button" type="button">{{ selectedLocation }}</button>
      <button class="ghost-button" type="button">{{ temperatureUnit }}°</button>
      <button class="primary-button" type="button" @click="$emit('open-dashboard')">{{ labels.dashboard }}</button>
      <button class="primary-button" type="button" @click="$emit('home')">{{ labels.home }}</button>
      <button class="primary-button" type="button" @click="$emit('open-settings')">{{ labels.settings }}</button>
      <button v-if="!isAuthenticated" class="primary-button" type="button" @click="$emit('open-auth')">{{ labels.signIn }}</button>
      <button v-else class="ghost-button" type="button" @click="$emit('logout')">{{ userEmail || labels.signOutFallback }}</button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  selectedLocation: { type: String, required: true },
  temperatureUnit: { type: String, required: true },
  isAuthenticated: { type: Boolean, default: false },
  userEmail: { type: String, default: '' },
  labels: { type: Object, required: true },
})
defineEmits(['open-settings', 'open-auth', 'open-dashboard', 'home', 'logout'])
</script>

<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; }
.header { display: flex; align-items: center; justify-content: space-between; gap: 16px; border-radius: 18px; padding: 18px 20px; }
.brand { display: flex; align-items: center; gap: 14px; }
.brand-mark { width: 44px; height: 44px; display: grid; place-items: center; border-radius: 12px; background: #e8f3ea; border: 1px solid #b9d0bc; color: #2f7d4b; font-weight: 700; letter-spacing: 0.04em; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h1, p { margin: 0; }
h1 { font-size: 1.4rem; }
.header-right { margin-left: auto; }
.header-right { display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-end; }
.ghost-button, .primary-button { border-radius: 12px; padding: 10px 14px; cursor: pointer; border: 1px solid #cfd8cf; background: #ffffff; color: #23402e; }
.primary-button { border-color: #7ab48a; background: #2f7d4b; color: white; }
@media (max-width: 960px) {
  .header { align-items: flex-start; flex-wrap: wrap; }
  .brand { flex: 1 1 auto; }
  .header-right { margin-left: 0; justify-content: flex-start; }
}
@media (max-width: 640px) {
  .header { flex-direction: column; align-items: stretch; }
  .header-right button { width: 100%; }
}
</style>
