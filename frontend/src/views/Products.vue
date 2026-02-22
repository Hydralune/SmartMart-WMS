<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">商品管理</div>
        <div class="page-subtitle">维护商品基础信息与库存上下限</div>
      </div>
      <el-button type="primary" :icon="Plus" class="btn-glow" @click="openDialog()">新增商品</el-button>
    </div>

    <div class="filter-bar fade-in-up">
      <el-input v-model="search" placeholder="搜索商品名称..." prefix-icon="Search"
        clearable style="width:240px" @input="load" />
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="商品名称" min-width="140" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="spec" label="规格" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column label="库存下限" width="90">
          <template #default="{ row }"><span class="text-danger">{{ row.stock_min }}</span></template>
        </el-table-column>
        <el-table-column label="库存上限" width="90">
          <template #default="{ row }"><span class="text-warning">{{ row.stock_max }}</span></template>
        </el-table-column>
        <el-table-column label="操作" width="140" v-if="isAdmin">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑商品' : '新增商品'" width="480px" destroy-on-close append-to-body>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="form.spec" placeholder="如 500ml/瓶" />
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="form.unit" placeholder="如 瓶" />
        </el-form-item>
        <el-form-item label="库存下限">
          <el-input-number v-model="form.stock_min" :min="0" style="width:100%" />
        </el-form-item>
        <el-form-item label="库存上限">
          <el-input-number v-model="form.stock_max" :min="0" style="width:100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productsApi } from '@/api'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const isAdmin = auth.isAdmin
const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()
const search = ref('')
const form = ref({ id: null, name: '', category: '', spec: '', unit: '', stock_min: 0, stock_max: 9999 })
const rules = {
  name:     [{ required: true, message: '请填写商品名称' }],
  category: [{ required: true, message: '请填写分类' }],
}

async function load() {
  loading.value = true
  try { list.value = await productsApi.list({ q: search.value }) } finally { loading.value = false }
}

function openDialog(row = null) {
  dialogVisible.value = true
  form.value = row
    ? { ...row }
    : { id: null, name: '', category: '', spec: '', unit: '', stock_min: 0, stock_max: 9999 }
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (form.value.id) await productsApi.update(form.value.id, form.value)
    else await productsApi.create(form.value)
    ElMessage.success('保存成功')
    dialogVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.msg || '保存失败')
  } finally {
    submitting.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确认删除商品「${row.name}」？`, '删除确认', { type: 'warning' })
  await productsApi.remove(row.id)
  ElMessage.success('删除成功')
  load()
}

onMounted(load)
</script>

<style scoped>
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.text-danger  { color: var(--danger); font-weight: 600; }
.text-warning { color: var(--warning); font-weight: 600; }
</style>
