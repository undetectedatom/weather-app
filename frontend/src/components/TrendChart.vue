<template>
  <div class="trend-shell">
    <canvas ref="canvasRef" aria-hidden="true"></canvas>
  </div>
</template>

<script setup>
import { Chart, Filler, LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Filler)

const props = defineProps({
  labels: { type: Array, required: true },
  values: { type: Array, required: true },
  lineColor: { type: String, default: '#2f7d4b' },
  fillTop: { type: String, default: 'rgba(47, 125, 75, 0.28)' },
  fillBottom: { type: String, default: 'rgba(47, 125, 75, 0.03)' },
})

const canvasRef = ref(null)
let chart = null

function buildGradient(context, chartArea) {
  const gradient = context.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)
  gradient.addColorStop(0, props.fillTop)
  gradient.addColorStop(1, props.fillBottom)
  return gradient
}

function buildConfig() {
  return {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [{
        data: props.values,
        borderColor: props.lineColor,
        borderWidth: 3,
        fill: true,
        spanGaps: true,
        tension: 0.42,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHitRadius: 14,
        pointBackgroundColor: props.lineColor,
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        backgroundColor(context) {
          const chartArea = context.chart.chartArea
          if (!chartArea) return props.fillBottom
          return buildGradient(context.chart.ctx, chartArea)
        },
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          displayColors: false,
          backgroundColor: 'rgba(22, 31, 24, 0.92)',
          cornerRadius: 10,
          padding: 10,
          caretPadding: 8,
          callbacks: {
            title(items) {
              return items[0]?.label ?? ''
            },
            label(item) {
              return `Avg ${Math.round(item.raw)}°`
            },
          },
        },
      },
      layout: {
        padding: { top: 10, right: 4, bottom: 2, left: 4 },
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false,
          },
          ticks: {
            color: '#6f8174',
            font: { size: 11 },
            maxRotation: 0,
            autoSkipPadding: 18,
          },
          border: { display: false },
        },
        y: {
          grace: '12%',
          grid: {
            color: 'rgba(111, 129, 116, 0.18)',
            drawTicks: false,
          },
          ticks: {
            display: false,
            count: 4,
          },
          border: { display: false },
        },
      },
    },
  }
}

function renderChart() {
  if (!canvasRef.value) return
  if (chart) {
    chart.destroy()
    chart = null
  }
  chart = new Chart(canvasRef.value, buildConfig())
}

onMounted(() => {
  renderChart()
})

watch(() => [props.labels, props.values, props.lineColor, props.fillTop, props.fillBottom], () => {
  renderChart()
}, { deep: true })

onBeforeUnmount(() => {
  if (chart) chart.destroy()
})
</script>

<style scoped>
.trend-shell {
  position: relative;
  height: 12rem;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
