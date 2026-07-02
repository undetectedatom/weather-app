<template>
  <section class="panel dashboard-panel">
    <div class="dashboard-header">
      <div>
        <p class="eyebrow">User workspace</p>
        <h2>Saved weather records</h2>
      </div>
      <button class="back-button" type="button" @click="$emit('back')">Back to home</button>
    </div>

    <div class="dashboard-summary">
      <article class="summary-card">
        <p class="summary-label">Records</p>
        <strong>{{ records.length }}</strong>
      </article>
      <article class="summary-card">
        <p class="summary-label">Unit</p>
        <strong>{{ temperatureUnit }}°</strong>
      </article>
      <article class="summary-card">
        <p class="summary-label">Export</p>
        <strong>JSON / CSV / XML / Markdown</strong>
      </article>
    </div>

    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>Location</th>
            <th>Date range</th>
            <th>Temp</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.id">
            <td>{{ record.location }}</td>
            <td>{{ record.startDate }} to {{ record.endDate }}</td>
            <td>{{ record.temperature }}</td>
            <td>{{ record.status }}</td>
            <td class="action-cell">
              <button type="button" @click="$emit('update-record', record.id)">Edit</button>
              <button type="button" @click="$emit('delete-record', record.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <section class="export-panel">
      <div>
        <p class="eyebrow">Export data</p>
        <h3>Download saved weather records</h3>
      </div>
      <div class="export-actions">
        <button type="button" @click="$emit('export-records', 'json')">JSON</button>
        <button type="button" @click="$emit('export-records', 'csv')">CSV</button>
        <button type="button" @click="$emit('export-records', 'xml')">XML</button>
        <button type="button" @click="$emit('export-records', 'markdown')">Markdown</button>
      </div>
    </section>
  </section>
</template>

<script setup>
defineProps({
  records: {
    type: Array,
    required: true,
  },
  temperatureUnit: {
    type: String,
    required: true,
  },
})

defineEmits(['back', 'update-record', 'delete-record', 'export-records'])
</script>

<style scoped>
.panel {
  background: #ffffff;
  border: 1px solid #cfd8cf;
  border-radius: 18px;
  padding: 22px;
}

.dashboard-panel {
  display: grid;
  gap: 16px;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #6f8174;
}

h2,
h3,
p {
  margin: 0;
}

.back-button,
.export-actions button,
.action-cell button {
  border: 1px solid #cfd8cf;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  background: #ffffff;
  color: #23402e;
}

.dashboard-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.summary-card {
  border: 1px solid #cfd8cf;
  border-radius: 14px;
  padding: 16px;
  background: #f7faf7;
}

.summary-label {
  color: #6f8174;
  margin-bottom: 8px;
}

.table-shell {
  overflow-x: auto;
  border: 1px solid #cfd8cf;
  border-radius: 14px;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

th,
td {
  padding: 14px 12px;
  border-bottom: 1px solid #dbe4dc;
  text-align: left;
}

th {
  background: #f5f8f4;
  color: #4f6754;
}

.action-cell {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.export-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid #cfd8cf;
  border-radius: 14px;
  padding: 16px;
  background: #f7faf7;
}

.export-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

@media (max-width: 960px) {
  .dashboard-summary,
  .export-panel {
    grid-template-columns: 1fr;
    flex-direction: column;
    align-items: stretch;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
  }

  .action-cell {
    flex-direction: column;
  }

  .export-actions button,
  .back-button {
    width: 100%;
  }
}
</style>
