<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">库存管理</div>
        <div class="page-subtitle">实时库存明细，支持搜索与预警</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar fade-in-up">
      <el-input v-model="search" placeholder="搜索商品名称..." prefix-icon="Search"
        clearable style="width:240px" @input="load" />
      <el-select v-model="category" placeholder="全部分类" clearable style="width:160px" @change="load">
        <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
      </el-select>
      <el-button :icon="Refresh" @click="load">刷新</el-button>
    </div>

    <!-- Table -->
    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="product_name" label="商品名称" min-width="140" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="spec" label="规格" width="100" />
        <el-table-column prop="batch_no" label="批次" width="120" />
        <el-table-column label="库存数量" width="120">
          <template #default="{ row }">
            <span :class="stockClass(row)" class="stock-num">{{ row.quantity }}</span>
            <span class="stock-unit"> {{ row.unit }}</span>
          </template>
        </el-table-column>
        <el-table-column label="库存状态" width="110">
          <template #default="{ row }">
            <el-tag :type="stockTagType(row)" size="small">{{ stockLabel(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="保质期剩余" width="120">
          <template #default="{ row }">
            <span v-if="row.days_until_expire !== null"
              :class="{ 'expire-warn': row.days_until_expire < 30 }">
              {{ row.days_until_expire }} 天
            </span>
            <span v-else class="text-muted">—</span>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="货架位置" width="100" />
        <el-table-column label="上/下限" width="100">
          <template #default="{ row }">
            <span class="text-muted">{{ row.stock_min }} / {{ row.stock_max }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { inventoryApi } from '@/api'

const list = ref([])
const loading = ref(false)
const search = ref('')
const category = ref('')
const categories = ref([])

async function load() {
  loading.value = true
  try {
    const data = await inventoryApi.list({ q: search.value, category: category.value })
    list.value = data
    categories.value = [...new Set(data.map(i => i.category).filter(Boolean))]
  } finally {
    loading.value = false
  }
}

function stockClass(row) {
  if (row.quantity < row.stock_min) return 'stock-low'
  if (row.quantity > row.stock_max) return 'stock-high'
  return 'stock-ok'
}
function stockTagType(row) {
  if (row.quantity < row.stock_min) return 'danger'
  if (row.quantity > row.stock_max) return 'warning'
  return 'success'
}
function stockLabel(row) {
  if (row.quantity < row.stock_min) return '库存不足'
  if (row.quantity > row.stock_max) return '滞销风险'
  return '正常'
}

onMounted(load)
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; align-items: center; margin-bottom: 16px; flex-wrap: wrap; }
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.stock-num { font-weight: 700; font-size: 15px; }
.stock-unit { font-size: 12px; color: var(--text-muted); }
.stock-low  { color: var(--danger); }
.stock-high { color: var(--warning); }
.stock-ok   { color: var(--success); }
.expire-warn { color: var(--danger); font-weight: 600; }
.text-muted { color: var(--text-muted); font-size: 13px; }
</style>
