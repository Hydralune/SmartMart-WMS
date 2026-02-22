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
  { label: '商品种类', value: '-', icon: 'Goods',        color: 'linear-gradient(135deg,#6366f1,#4f46e5)', trend: '', trendClass: '' },
  { label: '今日入库', value: '-', icon: 'Download',     color: 'linear-gradient(135deg,#10b981,#059669)', trend: '', trendClass: '' },
  { label: '今日出库', value: '-', icon: 'Upload',       color: 'linear-gradient(135deg,#f59e0b,#d97706)', trend: '', trendClass: '' },
  { label: '预警商品', value: '-', icon: 'Warning',      color: 'linear-gradient(135deg,#ef4444,#dc2626)', trend: '', trendClass: '' },
])

const chartTheme = {
  textStyle: { color: '#94a3b8' },
  axisLine: { lineStyle: { color: '#334155' } },
  splitLine: { lineStyle: { color: '#1e293b' } },
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
    tooltip: { trigger: 'axis', backgroundColor: '#1e293b', borderColor: '#334155', textStyle: { color: '#f1f5f9' } },
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: { type: 'category', data: invStats.map(r => r.category), axisLine: chartTheme.axisLine, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'value', splitLine: chartTheme.splitLine, axisLabel: { color: '#94a3b8' } },
    series: [{
      type: 'bar', data: invStats.map(r => r.total), barMaxWidth: 48,
      itemStyle: { borderRadius: [6,6,0,0], color: new echarts.graphic.LinearGradient(0,0,0,1,[
        { offset: 0, color: '#818cf8' }, { offset: 1, color: '#4f46e5' }
      ])},
    }],
  })

  // Line chart
  const allDates = [...new Set([...trend.inbound.map(r=>r.date), ...trend.outbound.map(r=>r.date)])].sort()
  const line = echarts.init(lineRef.value)
  line.setOption({
    ...chartTheme,
    tooltip: { trigger: 'axis', backgroundColor: '#1e293b', borderColor: '#334155', textStyle: { color: '#f1f5f9' } },
    legend: { data: ['入库', '出库'], textStyle: { color: '#94a3b8' }, top: 0 },
    grid: { left: 40, right: 20, top: 36, bottom: 40 },
    xAxis: { type: 'category', data: allDates, axisLine: chartTheme.axisLine, axisLabel: { color: '#94a3b8', rotate: 30, fontSize: 10 } },
    yAxis: { type: 'value', splitLine: chartTheme.splitLine, axisLabel: { color: '#94a3b8' } },
    series: [
      { name: '入库', type: 'line', smooth: true, data: allDates.map(d => trend.inbound.find(r=>r.date===d)?.qty||0),
        lineStyle: { color: '#10b981', width: 2 }, itemStyle: { color: '#10b981' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(16,185,129,0.3)'},{offset:1,color:'rgba(16,185,129,0)'}]) } },
      { name: '出库', type: 'line', smooth: true, data: allDates.map(d => trend.outbound.find(r=>r.date===d)?.qty||0),
        lineStyle: { color: '#f59e0b', width: 2 }, itemStyle: { color: '#f59e0b' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(245,158,11,0.3)'},{offset:1,color:'rgba(245,158,11,0)'}]) } },
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
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
.kpi-icon {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
}
.kpi-value { font-size: 28px; font-weight: 700; color: var(--text); line-height: 1; }
.kpi-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.kpi-trend { margin-left: auto; font-size: 12px; font-weight: 600; }
.kpi-trend.up { color: var(--success); }
.kpi-trend.down { color: var(--danger); }

.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.chart-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; }
.chart-title { font-size: 14px; font-weight: 600; color: var(--text); margin-bottom: 16px; }
.chart { height: 260px; }

.warn-card { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3); border-radius: var(--radius); padding: 16px; }
.warn-header { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--danger); margin-bottom: 12px; }
.warn-icon { font-size: 18px; }
.warn-list { display: flex; flex-direction: column; gap: 8px; }
.warn-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; background: rgba(239,68,68,0.05); border-radius: 8px; }
.warn-name { font-size: 13px; color: var(--text); }
</style>
