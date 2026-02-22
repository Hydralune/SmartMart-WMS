<template>
  <div class="login-wrap">
    <!-- Animated background -->
    <div class="bg-orbs">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div class="login-card fade-in-up">
      <div class="login-logo">
        <div class="logo-icon"><el-icon><Box /></el-icon></div>
        <div>
          <div class="logo-name">SmartMart WMS</div>
          <div class="logo-sub">超市仓库管理系统</div>
        </div>
      </div>

      <el-form :model="form" :rules="rules" ref="formRef" class="login-form" @keyup.enter="submit">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" size="large"
            prefix-icon="Lock" show-password />
        </el-form-item>
        <el-button type="primary" size="large" class="login-btn btn-glow"
          :loading="loading" @click="submit">
          登 录
        </el-button>
      </el-form>

      <div class="login-hints">
        <div class="hint-title">测试账号</div>
        <div class="hints stagger">
          <div class="hint-item fade-in-up" v-for="h in hints" :key="h.role" @click="fillHint(h)">
            <span class="hint-role">{{ h.label }}</span>
            <span class="hint-user">{{ h.username }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()
const formRef = ref()
const loading = ref(false)
const form = ref({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const hints = [
  { label: '管理员', username: 'admin',     password: 'admin123' },
  { label: '仓库员', username: 'warehouse', password: 'warehouse123' },
  { label: '采购员', username: 'purchaser', password: 'purchaser123' },
]

function fillHint(h) {
  form.value.username = h.username
  form.value.password = h.password
}

async function submit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch {
    ElMessage.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: var(--bg); position: relative; overflow: hidden;
}

/* Orbs */
.bg-orbs { position: absolute; inset: 0; pointer-events: none; }
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.15;
  animation: float 8s ease-in-out infinite;
}
.orb-1 { width: 500px; height: 500px; background: var(--primary); top: -150px; left: -150px; animation-delay: 0s; }
.orb-2 { width: 400px; height: 400px; background: #06b6d4; bottom: -100px; right: -100px; animation-delay: 3s; }
.orb-3 { width: 300px; height: 300px; background: var(--success); top: 50%; left: 50%; animation-delay: 6s; }

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(30px, -30px) scale(1.05); }
  66%       { transform: translate(-20px, 20px) scale(0.95); }
}

.login-card {
  width: 420px; padding: 40px;
  background: rgba(30,41,59,0.8);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: 0 24px 64px rgba(0,0,0,0.4);
  position: relative; z-index: 1;
}

.login-logo { display: flex; align-items: center; gap: 14px; margin-bottom: 32px; }
.logo-icon {
  width: 48px; height: 48px; border-radius: 14px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  display: flex; align-items: center; justify-content: center;
  font-size: 24px;
  box-shadow: 0 8px 24px rgba(99,102,241,0.4);
}
.logo-name { font-size: 20px; font-weight: 700; color: var(--text); }
.logo-sub  { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

.login-form { display: flex; flex-direction: column; gap: 4px; }
.login-btn { width: 100%; margin-top: 8px; height: 44px; font-size: 15px; font-weight: 600; border-radius: 10px !important; }

.login-hints { margin-top: 28px; }
.hint-title { font-size: 12px; color: var(--text-muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
.hints { display: flex; gap: 8px; }
.hint-item {
  flex: 1; padding: 10px 12px; border-radius: 10px;
  background: var(--bg); border: 1px solid var(--border);
  cursor: pointer; transition: all var(--transition);
  display: flex; flex-direction: column; gap: 3px;
}
.hint-item:hover { border-color: var(--primary); background: rgba(99,102,241,0.08); }
.hint-role { font-size: 11px; color: var(--text-muted); }
.hint-user { font-size: 13px; font-weight: 600; color: var(--text); }
</style>
