<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">操作日志</div>
        <div class="page-subtitle">全量库存变动记录，支持 Excel 导出</div>
      </div>
      <el-button :icon="Download" @click="exportBackup" :loading="exporting">导出备份</el-button>
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column label="操作类型" width="100">
          <template #default="{ row }">
            <el-tag :type="actionTagType(row.action_type)" size="small">{{ row.action_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作详情" min-width="260" show-overflow-tooltip />
        <el-table-column prop="created_at" label="时间" width="180" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { logsApi } from '@/api'

const list = ref([])
const loading = ref(false)
const exporting = ref(false)

const actionMap = { '入库': '', '出库': 'warning', '盘点审核': 'success' }
function actionTagType(type) { return actionMap[type] ?? 'info' }

async function load() {
  loading.value = true
  try { list.value = await logsApi.list() } finally { loading.value = false }
}

async function exportBackup() {
  exporting.value = true
  try {
    const blob = await logsApi.exportBackup()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `smartmart_backup_${new Date().toISOString().slice(0,10)}.xlsx`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
</style>
