<template>
  <section class="panel dashboard-panel">
    <div class="dashboard-header">
      <div><p class="eyebrow">{{ labels.eyebrow }}</p><h2>{{ labels.title }}</h2></div>
      <button class="back-button" type="button" @click="$emit('back')">{{ labels.back }}</button>
    </div>
    <div class="dashboard-summary">
      <article class="summary-card"><p class="summary-label">{{ labels.records }}</p><strong>{{ records.length }}</strong></article>
      <article class="summary-card"><p class="summary-label">{{ labels.unit }}</p><strong>{{ temperatureUnit }}°</strong></article>
      <article class="summary-card"><p class="summary-label">{{ labels.export }}</p><strong>JSON / CSV / XML / Markdown</strong></article>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-else-if="loading" class="helper-text">{{ labels.loading }}</p>
    <p v-else-if="!records.length" class="helper-text">{{ labels.helper }}</p>
    <div v-else class="table-shell">
      <table>
        <thead><tr><th>{{ labels.location }}</th><th>{{ labels.dateRange }}</th><th>{{ labels.temp }}</th><th>{{ labels.actions }}</th></tr></thead>
        <tbody>
          <tr v-for="record in records" :key="record.id">
            <td :data-label="labels.location">{{ record.location }}</td>
            <td :data-label="labels.dateRange">{{ record.dateLabel }}</td>
            <td :data-label="labels.temp">{{ record.temperature }}</td>
            <td :data-label="labels.actions" class="action-cell"><button type="button" @click="$emit('update-record', record.id)">{{ labels.edit }}</button><button type="button" @click="$emit('delete-record', record.id)">{{ labels.delete }}</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <section class="export-panel">
      <div><p class="eyebrow">{{ labels.exportLabel }}</p><h3>{{ labels.exportTitle }}</h3></div>
      <div class="export-actions"><button type="button" @click="$emit('export-records', 'json')">JSON</button><button type="button" @click="$emit('export-records', 'csv')">CSV</button><button type="button" @click="$emit('export-records', 'xml')">XML</button><button type="button" @click="$emit('export-records', 'markdown')">Markdown</button></div>
    </section>
  </section>
</template>
<script setup>
defineProps({ records: { type: Array, required: true }, temperatureUnit: { type: String, required: true }, loading: { type: Boolean, default: false }, errorMessage: { type: String, default: '' }, labels: { type: Object, required: true } })
defineEmits(['back', 'update-record', 'delete-record', 'export-records'])
</script>
<style scoped>
.panel { background: #ffffff; border: 1px solid #cfd8cf; border-radius: 18px; padding: 22px; }
.dashboard-panel { display: grid; gap: 16px; }
.dashboard-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.eyebrow { margin: 0 0 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.16em; color: #6f8174; }
h2, h3, p { margin: 0; }
.back-button, .export-actions button, .action-cell button { border: 1px solid #cfd8cf; border-radius: 12px; padding: 10px 14px; cursor: pointer; background: #ffffff; color: #23402e; }
.dashboard-summary { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.summary-card { border: 1px solid #cfd8cf; border-radius: 14px; padding: 16px; background: #f7faf7; }
.summary-label { color: #6f8174; margin-bottom: 8px; }
.helper-text, .error-message { border-radius: 14px; padding: 14px; }
.helper-text { background: #f7faf7; border: 1px solid #dbe4dc; color: #4f6754; }
.error-message { background: #fff4f4; border: 1px solid #e4bbbb; color: #a63a3a; }
.table-shell { overflow-x: auto; border: 1px solid #cfd8cf; border-radius: 14px; }
table { width: 100%; border-collapse: collapse; min-width: 760px; }
th, td { padding: 14px 12px; border-bottom: 1px solid #dbe4dc; text-align: left; }
th { background: #f5f8f4; color: #4f6754; }
.action-cell { display: flex; gap: 8px; flex-wrap: wrap; }
.export-panel { display: flex; align-items: center; justify-content: space-between; gap: 12px; border: 1px solid #cfd8cf; border-radius: 14px; padding: 16px; background: #f7faf7; }
.export-actions { display: flex; gap: 8px; flex-wrap: wrap; }
@media (max-width: 960px) { .export-panel { flex-direction: column; align-items: stretch; } .dashboard-header { flex-wrap: wrap; align-items: center; } .export-actions button, .back-button { width: auto; } }
@media (max-width: 720px) { .dashboard-summary { grid-template-columns: 1fr; } .dashboard-header { flex-direction: column; align-items: stretch; } .action-cell { flex-direction: column; } .export-actions button, .back-button { width: 100%; } }
@media (max-width: 540px) {
  .panel { padding: 18px; }
  .table-shell { overflow: visible; border: 0; }
  table, thead, tbody, tr, th, td { display: block; width: 100%; }
  table { min-width: 0; }
  thead { display: none; }
  tbody { display: grid; gap: 12px; }
  tr { border: 1px solid #cfd8cf; border-radius: 14px; background: #f7faf7; padding: 14px; }
  td { border-bottom: 0; padding: 0; display: grid; gap: 4px; }
  td + td { margin-top: 12px; }
  td::before { content: attr(data-label); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: #6f8174; }
  .action-cell { margin-top: 2px; }
  .action-cell button { width: 100%; }
}
</style>
