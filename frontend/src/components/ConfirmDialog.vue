<template>
  <div class="overlay-shell" @click.self="$emit('close')">
    <section class="dialog panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">{{ labels.eyebrow }}</p>
          <h2>{{ labels.title }}</h2>
        </div>
      </div>
      <p class="message">{{ labels.message }}</p>
      <div class="actions">
        <button type="button" class="ghost-button" @click="$emit('close')">{{ labels.cancel }}</button>
        <button type="button" class="primary-button" @click="$emit('confirm')">{{ labels.confirm }}</button>
      </div>
    </section>
  </div>
</template>

<script setup>
defineProps({ labels: { type: Object, required: true } })
defineEmits(['close', 'confirm'])
</script>

<style scoped>
.overlay-shell { position: fixed; inset: 0; background: rgba(23, 49, 31, 0.24); display: flex; justify-content: center; align-items: center; z-index: 80; padding: 18px; }
.panel { width: min(420px, 100%); background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.panel-header { margin-bottom: 12px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, p { margin: 0; }
.message { color: #4f6754; line-height: 1.5; }
.actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px; }
.ghost-button, .primary-button { border-radius: 12px; padding: 10px 14px; cursor: pointer; border: 1px solid #cfd8cf; background: #ffffff; color: #23402e; }
.primary-button { border-color: #7ab48a; background: #2f7d4b; color: white; }
@media (max-width: 640px) { .actions { flex-direction: column; } .actions button { width: 100%; } }
</style>
