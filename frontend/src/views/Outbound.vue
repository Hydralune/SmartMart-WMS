<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">出库管理</div>
        <div class="page-subtitle">生成出库单，自动扣减库存</div>
      </div>
      <el-button type="primary" :icon="Plus" class="btn-glow" @click="openDialog">新增出库单</el-button>
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="单号" width="80" />
        <el-table-column prop="product_name" label="商品" min-width="140" />
        <el-table-column prop="quantity" label="出库数量" width="100" />
        <el-table-column prop="department" label="领用部门" width="120" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="created_at" label="出库时间" min-width="160" />
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" title="新增出库单" width="460px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="商品" prop="product_id">
          <el-select v-model="form.product_id" placeholder="选择商品" style="width:100%">
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="出库数量" prop="quantity">
          <el-input-number v-model="form.quantity" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="领用部门" prop="department">
          <el-input v-model="form.department" placeholder="如 收银台" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">确认出库</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { outboundApi, productsApi } from '@/api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()
const products = ref([])
const form = ref({ product_id: null, quantity: 1, department: '' })
const rules = {
  product_id: [{ required: true, message: '请选择商品' }],
  quantity:   [{ required: true, message: '请填写数量' }],
  department: [{ required: true, message: '请填写领用部门' }],
}

async function load() {
  loading.value = true
  try { list.value = await outboundApi.list() } finally { loading.value = false }
}

async function openDialog() {
  dialogVisible.value = true
  form.value = { product_id: null, quantity: 1, department: '' }
  products.value = await productsApi.list()
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await outboundApi.create(form.value)
    ElMessage.success('出库成功')
    dialogVisible.value = false
    load()
  } catch (e) {
    const msg = e.response?.data?.msg || '出库失败'
    ElMessageBox.alert(msg, '出库失败', { type: 'error' })
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
</style>
