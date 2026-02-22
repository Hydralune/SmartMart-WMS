<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">数据看板</div>
        <div class="page-subtitle">实时库存与出入库概览</div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid stagger">
      <div class="kpi-card fade-in-up" v-for="k in kpis" :key="k.label">
        <div class="kpi-icon" :style="{ background: k.color }">
          <el-icon><component :is="k.icon" /></el-icon>
        </div>
        <div class="kpi-body">
          <div class="kpi-value">{{ k.value }}</div>
          <div class="kpi-label">{{ k.label }}</div>
        </div>
        <div class="kpi-trend" :class="k.trendClass">{{ k.trend }}</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <div class="chart-card fade-in-up">
        <div class="chart-title">各分类库存占比</div>
        <div ref="barRef" class="chart"></div>
      </div>
      <div class="chart-card fade-in-up">
        <div class="chart-title">近30天出入库趋势</div>
        <div ref="lineRef" class="chart"></div>
      </div>
    </div>

    <!-- Low stock warnings -->
    <div class="warn-card fade-in-up" v-if="lowStock.length">
      <div class="warn-header">
        <el-icon class="warn-icon"><Warning /></el-icon>
        <span>库存预警（{{ lowStock.length }} 项低于下限）</span>
      </div>
      <div class="warn-list">
        <div class="warn-item" v-for="item in lowStock" :key="item.id">
          <span class="warn-name">{{ item.product_name }}</span>
          <el-tag type="danger" size="small">库存 {{ item.quantity }} / 下限 {{ item.stock_min }}</el-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { statsApi, inventoryApi } from '@/api'

const barRef = ref()
const lineRef = ref()
const lowStock = ref([])
const kpis = ref([
  { label: '商品种类', value: '-', icon: 'Goods',    color: 'linear-gradient(135deg,#2563eb,#1d4ed8)', trend: '', trendClass: '' },
  { label: '今日入库', value: '-', icon: 'Download', color: 'linear-gradient(135deg,#7c3aed,#6d28d9)', trend: '', trendClass: '' },
  { label: '今日出库', value: '-', icon: 'Upload',   color: 'linear-gradient(135deg,#0891b2,#0e7490)', trend: '', trendClass: '' },
  { label: '预警商品', value: '-', icon: 'Warning',  color: 'linear-gradient(135deg,#dc2626,#b91c1c)', trend: '', trendClass: '' },
])

const chartTheme = {
  textStyle: { color: '#64748b' },
  axisLine: { lineStyle: { color: '#e2e8f0' } },
  splitLine: { lineStyle: { color: '#f1f5f9' } },
}

onMounted(async () => {
  const [invStats, trend, invList] = await Promise.all([
    statsApi.inventory(),
    statsApi.trend(),
    inventoryApi.list(),
  ])

  // Low stock
  lowStock.value = invList.filter(i => i.quantity < i.stock_min)
  kpis.value[0].value = new Set(invList.map(i => i.product_id)).size
  kpis.value[3].value = lowStock.value.length

  // Today inbound/outbound
  const today = new Date().toISOString().slice(0, 10)
  const todayIn  = trend.inbound.find(r => r.date === today)?.qty  || 0
  const todayOut = trend.outbound.find(r => r.date === today)?.qty || 0
  kpis.value[1].value = todayIn
  kpis.value[2].value = todayOut

  // Bar chart
  const bar = echarts.init(barRef.value)
  bar.setOption({
    ...chartTheme,
    tooltip: { trigger: 'axis', backgroundColor: '#fff', borderColor: '#e2e8f0', textStyle: { color: '#0f172a' }, extraCssText: 'box-shadow:0 4px 16px rgba(0,0,0,0.1);border-radius:8px;' },
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: { type: 'category', data: invStats.map(r => r.category), axisLine: chartTheme.axisLine, axisLabel: { color: '#64748b' } },
    yAxis: { type: 'value', splitLine: chartTheme.splitLine, axisLabel: { color: '#64748b' } },
    series: [{
      type: 'bar', data: invStats.map(r => r.total), barMaxWidth: 48,
      itemStyle: { borderRadius: [6,6,0,0], color: new echarts.graphic.LinearGradient(0,0,0,1,[
        { offset: 0, color: '#3b82f6' }, { offset: 1, color: '#2563eb' }
      ])},
    }],
  })

  // Line chart
  const allDates = [...new Set([...trend.inbound.map(r=>r.date), ...trend.outbound.map(r=>r.date)])].sort()
  const line = echarts.init(lineRef.value)
  line.setOption({
    ...chartTheme,
    tooltip: { trigger: 'axis', backgroundColor: '#fff', borderColor: '#e2e8f0', textStyle: { color: '#0f172a' }, extraCssText: 'box-shadow:0 4px 16px rgba(0,0,0,0.1);border-radius:8px;' },
    legend: { data: ['入库', '出库'], textStyle: { color: '#64748b' }, top: 0 },
    grid: { left: 40, right: 20, top: 36, bottom: 40 },
    xAxis: { type: 'category', data: allDates, axisLine: chartTheme.axisLine, axisLabel: { color: '#64748b', rotate: 30, fontSize: 10 } },
    yAxis: { type: 'value', splitLine: chartTheme.splitLine, axisLabel: { color: '#64748b' } },
    series: [
      { name: '入库', type: 'line', smooth: true, data: allDates.map(d => trend.inbound.find(r=>r.date===d)?.qty||0),
        lineStyle: { color: '#2563eb', width: 2.5 }, itemStyle: { color: '#2563eb' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(37,99,235,0.15)'},{offset:1,color:'rgba(37,99,235,0)'}]) } },
      { name: '出库', type: 'line', smooth: true, data: allDates.map(d => trend.outbound.find(r=>r.date===d)?.qty||0),
        lineStyle: { color: '#7c3aed', width: 2.5 }, itemStyle: { color: '#7c3aed' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(124,58,237,0.15)'},{offset:1,color:'rgba(124,58,237,0)'}]) } },
    ],
  })

  window.addEventListener('resize', () => { bar.resize(); line.resize() })
})
</script>

<style scoped>
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; display: flex; align-items: center; gap: 16px;
  transition: transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow-sm);
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.kpi-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #fff; flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.kpi-value { font-size: 30px; font-weight: 700; color: var(--text); line-height: 1; }
.kpi-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.kpi-trend { margin-left: auto; font-size: 12px; font-weight: 600; }
.kpi-trend.up { color: var(--success); }
.kpi-trend.down { color: var(--danger); }

.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.chart-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px;
  box-shadow: var(--shadow-sm);
}
.chart-title { font-size: 14px; font-weight: 600; color: var(--text); margin-bottom: 16px; }
.chart { height: 260px; }

.warn-card {
  background: var(--danger-light); border: 1px solid #fecaca;
  border-radius: var(--radius); padding: 16px;
  box-shadow: var(--shadow-sm);
}
.warn-header { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--danger); margin-bottom: 12px; }
.warn-icon { font-size: 18px; }
.warn-list { display: flex; flex-direction: column; gap: 8px; }
.warn-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: rgba(255,255,255,0.6); border-radius: 8px;
  border: 1px solid #fecaca;
}
.warn-name { font-size: 13px; color: var(--text); font-weight: 500; }
</style>
