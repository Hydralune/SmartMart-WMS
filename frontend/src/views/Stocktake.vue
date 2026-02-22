<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">库存盘点</div>
        <div class="page-subtitle">录入实际库存，管理员审核后调整</div>
      </div>
      <el-button type="primary" :icon="Plus" class="btn-glow" @click="openDialog">新增盘点</el-button>
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="单号" width="80" />
        <el-table-column prop="product_name" label="商品" min-width="140" />
        <el-table-column prop="book_qty" label="账面库存" width="100" />
        <el-table-column prop="actual_qty" label="实际库存" width="100" />
        <el-table-column label="差异" width="100">
          <template #default="{ row }">
            <span :class="row.diff > 0 ? 'diff-pos' : row.diff < 0 ? 'diff-neg' : ''">
              {{ row.diff > 0 ? '+' : '' }}{{ row.diff }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'approved' ? 'success' : 'warning'" size="small">
              {{ row.status === 'approved' ? '已审核' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="created_at" label="时间" min-width="160" />
        <el-table-column label="操作" width="100" v-if="isAdmin">
          <template #default="{ row }">
            <el-button v-if="row.status === 'pending'" type="success" size="small"
              @click="approve(row)">审核</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" title="新增盘点单" width="420px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="商品" prop="product_id">
          <el-select v-model="form.product_id" placeholder="选择商品" style="width:100%">
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="实际库存" prop="actual_qty">
          <el-input-number v-model="form.actual_qty" :min="0" style="width:100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">提交盘点</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { stocktakeApi, productsApi } from '@/api'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const isAdmin = auth.isAdmin
const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()
const products = ref([])
const form = ref({ product_id: null, actual_qty: 0 })
const rules = {
  product_id: [{ required: true, message: '请选择商品' }],
  actual_qty: [{ required: true, message: '请填写实际库存' }],
}

async function load() {
  loading.value = true
  try { list.value = await stocktakeApi.list() } finally { loading.value = false }
}

async function openDialog() {
  dialogVisible.value = true
  form.value = { product_id: null, actual_qty: 0 }
  products.value = await productsApi.list()
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await stocktakeApi.create(form.value)
    ElMessage.success('盘点单已提交')
    dialogVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.msg || '提交失败')
  } finally {
    submitting.value = false
  }
}

async function approve(row) {
  await stocktakeApi.approve(row.id)
  ElMessage.success('审核通过，库存已调整')
  load()
}

onMounted(load)
</script>

<style scoped>
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.diff-pos { color: var(--success); font-weight: 700; }
.diff-neg { color: var(--danger); font-weight: 700; }
</style>
