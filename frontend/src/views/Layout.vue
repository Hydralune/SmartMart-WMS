<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed }">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <el-icon><Box /></el-icon>
        </div>
        <transition name="fade">
          <span v-if="!collapsed" class="logo-text">SmartMart</span>
        </transition>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
          <transition name="fade">
            <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
          </transition>
          <span v-if="!collapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info" v-if="!collapsed">
          <div class="user-avatar">{{ auth.user?.username?.[0]?.toUpperCase() }}</div>
          <div class="user-meta">
            <div class="user-name">{{ auth.user?.username }}</div>
            <div class="user-role">{{ roleLabel }}</div>
          </div>
        </div>
        <el-tooltip :content="collapsed ? '展开' : '收起'" placement="right">
          <button class="collapse-btn" @click="collapsed = !collapsed">
            <el-icon><ArrowLeft v-if="!collapsed" /><ArrowRight v-else /></el-icon>
          </button>
        </el-tooltip>
      </div>
    </aside>

    <!-- Main -->
    <div class="main-wrap">
      <header class="topbar">
        <div class="topbar-left">
          <h1 class="topbar-title">{{ $route.meta.title }}</h1>
          <div class="breadcrumb">
            <span>SmartMart WMS</span>
            <el-icon><ArrowRight /></el-icon>
            <span>{{ $route.meta.title }}</span>
          </div>
        </div>
        <div class="topbar-right">
          <el-tooltip content="退出登录" placement="bottom">
            <button class="logout-btn" @click="logout">
              <el-icon><SwitchButton /></el-icon>
            </button>
          </el-tooltip>
        </div>
      </header>

      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const router = useRouter()
const collapsed = ref(false)

const roleMap = { admin: '管理员', warehouse: '仓库员', purchaser: '采购员' }
const roleLabel = computed(() => roleMap[auth.role] || auth.role)

const navItems = [
  { path: '/dashboard', icon: 'DataAnalysis', label: '数据看板' },
  { path: '/inventory',  icon: 'Goods',        label: '库存管理' },
  { path: '/inbound',    icon: 'Download',      label: '入库管理' },
  { path: '/outbound',   icon: 'Upload',        label: '出库管理' },
  { path: '/stocktake',  icon: 'List',          label: '库存盘点' },
  { path: '/products',   icon: 'ShoppingBag',   label: '商品管理' },
  { path: '/suppliers',  icon: 'OfficeBuilding', label: '供应商' },
  { path: '/logs',       icon: 'Document',      label: '操作日志' },
]

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; height: 100vh; overflow: hidden; }

/* Sidebar */
.sidebar {
  width: 240px; min-width: 240px;
  background: #0d1b2e;
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  transition: width var(--transition), min-width var(--transition);
  overflow: hidden;
}
.sidebar.collapsed { width: 64px; min-width: 64px; }

.sidebar-logo {
  display: flex; align-items: center; gap: 12px;
  padding: 20px 16px; border-bottom: 1px solid var(--border);
}
.logo-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99,102,241,0.4);
}
.logo-text { font-size: 16px; font-weight: 700; color: var(--text); white-space: nowrap; }

.sidebar-nav { flex: 1; padding: 12px 8px; display: flex; flex-direction: column; gap: 4px; overflow-y: auto; }

.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px; border-radius: 10px;
  color: var(--text-muted); text-decoration: none;
  transition: all var(--transition); white-space: nowrap;
  position: relative; overflow: hidden;
}
.nav-item::before {
  content: ''; position: absolute; left: 0; top: 50%;
  transform: translateY(-50%); width: 3px; height: 0;
  background: var(--primary); border-radius: 0 3px 3px 0;
  transition: height var(--transition);
}
.nav-item:hover { background: rgba(99,102,241,0.1); color: var(--text); }
.nav-item.active { background: rgba(99,102,241,0.15); color: var(--primary-light); }
.nav-item.active::before { height: 60%; }
.nav-icon { font-size: 18px; flex-shrink: 0; }
.nav-label { font-size: 14px; font-weight: 500; }
.nav-badge {
  margin-left: auto; background: var(--danger);
  color: #fff; font-size: 11px; padding: 1px 6px;
  border-radius: 10px; font-weight: 600;
}

.sidebar-footer {
  padding: 12px 8px; border-top: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px;
}
.user-info { display: flex; align-items: center; gap: 10px; flex: 1; overflow: hidden; }
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.user-name { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: var(--text-muted); }
.collapse-btn {
  width: 32px; height: 32px; border-radius: 8px; border: 1px solid var(--border);
  background: transparent; color: var(--text-muted); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition); flex-shrink: 0;
}
.collapse-btn:hover { background: var(--bg-card2); color: var(--text); }

/* Main */
.main-wrap { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

.topbar {
  height: 60px; padding: 0 24px;
  background: rgba(15,23,42,0.8); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.topbar-title { font-size: 16px; font-weight: 700; color: var(--text); }
.breadcrumb { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-muted); margin-top: 2px; }
.logout-btn {
  width: 36px; height: 36px; border-radius: 10px; border: 1px solid var(--border);
  background: transparent; color: var(--text-muted); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition);
}
.logout-btn:hover { background: rgba(239,68,68,0.1); color: var(--danger); border-color: var(--danger); }

.content { flex: 1; overflow-y: auto; }

/* Page transition */
.page-enter-active, .page-leave-active { transition: all 0.25s ease; }
.page-enter-from { opacity: 0; transform: translateY(12px); }
.page-leave-to   { opacity: 0; transform: translateY(-8px); }

/* Fade transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
