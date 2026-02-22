<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">入库管理</div>
        <div class="page-subtitle">新增入库单，自动更新库存</div>
      </div>
      <el-button type="primary" :icon="Plus" class="btn-glow" @click="openDialog">新增入库单</el-button>
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="单号" width="80" />
        <el-table-column prop="product_name" label="商品" min-width="140" />
        <el-table-column prop="supplier_name" label="供应商" min-width="120" />
        <el-table-column prop="batch_no" label="批次" width="120" />
        <el-table-column prop="quantity" label="入库数量" width="100" />
        <el-table-column prop="expire_date" label="保质期" width="120" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="created_at" label="入库时间" min-width="160" />
      </el-table>
    </div>

    <!-- Dialog -->
    <el-dialog v-model="dialogVisible" title="新增入库单" width="500px" destroy-on-close append-to-body>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="供应商" prop="supplier_id">
          <el-select v-model="form.supplier_id" placeholder="选择供应商" style="width:100%">
            <el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品" prop="product_id">
          <el-select v-model="form.product_id" placeholder="选择商品" style="width:100%">
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="批次号" prop="batch_no">
          <el-input v-model="form.batch_no" placeholder="如 BATCH-2024-001" />
        </el-form-item>
        <el-form-item label="入库数量" prop="quantity">
          <el-input-number v-model="form.quantity" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="保质期" prop="expire_date">
          <el-date-picker v-model="form.expire_date" type="date" value-format="YYYY-MM-DD"
            placeholder="选择保质期" style="width:100%" />
        </el-form-item>
        <el-form-item label="货架位置">
          <el-input v-model="form.location" placeholder="如 A-01" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">确认入库</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { inboundApi, suppliersApi, productsApi } from '@/api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()
const suppliers = ref([])
const products = ref([])

const form = ref({ supplier_id: null, product_id: null, batch_no: '', quantity: 1, expire_date: '', location: '' })
const rules = {
  supplier_id: [{ required: true, message: '请选择供应商' }],
  product_id:  [{ required: true, message: '请选择商品' }],
  quantity:    [{ required: true, message: '请填写数量' }],
}

async function load() {
  loading.value = true
  try { list.value = await inboundApi.list() } finally { loading.value = false }
}

async function openDialog() {
  dialogVisible.value = true
  form.value = { supplier_id: null, product_id: null, batch_no: '', quantity: 1, expire_date: '', location: '' }
  const [s, p] = await Promise.all([suppliersApi.list(), productsApi.list()])
  suppliers.value = s
  products.value = p
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await inboundApi.create(form.value)
    ElMessage.success('入库成功')
    dialogVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.msg || '入库失败')
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
</style>
