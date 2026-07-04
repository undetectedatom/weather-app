<template>
  <section class="info-panel">
    <div class="panel-copy">
      <p class="eyebrow">Assessment Info</p>
      <h2>Project context</h2>
      <p class="summary">
        HelloWeather is a full-stack weather application built for the PM Accelerator AI Engineer Intern technical assessment.
      </p>
    </div>

    <div class="detail-grid">
      <article class="detail-card">
        <p class="label">Project author</p>
        <strong>{{ creatorName }}</strong>
      </article>

      <article class="detail-card detail-card-wide">
        <p class="label">About PM Accelerator</p>
        <p>
          PM Accelerator is a product management career platform that offers training, coaching, free resources,
          and community support for aspiring and current product managers.
        </p>
        <a href="https://www.pmaccelerator.io/" target="_blank" rel="noreferrer">pmaccelerator.io</a>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  creatorName: { type: String, required: true },
})
</script>

<style scoped>
.info-panel {
  display: grid;
  gap: 16px;
  padding: 20px;
  border-radius: 18px;
  border: 1px solid #cfd8cf;
  background: linear-gradient(180deg, #fcfefc 0%, #f3f8f3 100%);
}

.panel-copy {
  display: grid;
  gap: 8px;
}

.eyebrow,
.label {
  margin: 0;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #6f8174;
}

h2,
p {
  margin: 0;
}

h2 {
  font-size: 1.2rem;
}

.summary {
  color: #385342;
  max-width: 72ch;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.detail-card {
  display: grid;
  gap: 8px;
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #d5e0d6;
  background: rgba(255, 255, 255, 0.9);
}

.detail-card-wide p:last-of-type {
  color: #385342;
}

a {
  color: #1d6a3b;
  font-weight: 600;
}

@media (max-width: 720px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
