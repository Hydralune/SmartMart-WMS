<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">供应商管理</div>
        <div class="page-subtitle">维护供应商信息与合作状态</div>
      </div>
      <el-button type="primary" :icon="Plus" class="btn-glow" @click="openDialog()">新增供应商</el-button>
    </div>

    <div class="table-card fade-in-up">
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="供应商名称" min-width="140" />
        <el-table-column prop="contact" label="联系人" width="100" />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="category" label="供应商品类" min-width="140" />
        <el-table-column label="合作状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
              {{ row.status === 'active' ? '合作中' : '已停止' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)" v-if="isAdmin">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑供应商' : '新增供应商'" width="480px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="form.contact" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="供应商品类">
          <el-input v-model="form.category" placeholder="如 饮料,零食" />
        </el-form-item>
        <el-form-item label="合作状态">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="合作中" value="active" />
            <el-option label="已停止" value="inactive" />
          </el-select>
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
import { suppliersApi } from '@/api'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const isAdmin = auth.isAdmin
const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()
const form = ref({ id: null, name: '', contact: '', phone: '', category: '', status: 'active' })
const rules = { name: [{ required: true, message: '请填写供应商名称' }] }

async function load() {
  loading.value = true
  try { list.value = await suppliersApi.list() } finally { loading.value = false }
}

function openDialog(row = null) {
  dialogVisible.value = true
  form.value = row ? { ...row } : { id: null, name: '', contact: '', phone: '', category: '', status: 'active' }
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (form.value.id) await suppliersApi.update(form.value.id, form.value)
    else await suppliersApi.create(form.value)
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
  await ElMessageBox.confirm(`确认删除供应商「${row.name}」？`, '删除确认', { type: 'warning' })
  await suppliersApi.remove(row.id)
  ElMessage.success('删除成功')
  load()
}

onMounted(load)
</script>

<style scoped>
.table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
</style>
