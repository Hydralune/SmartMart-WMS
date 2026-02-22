import { createRouter, createWebHistory } from 'vue-router'
import { getActivePinia } from 'pinia'
import { useAuthStore } from '@/store/auth'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const routes = [
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard',  component: () => import('@/views/Dashboard.vue'),  meta: { title: '数据看板' } },
      { path: 'inventory',  component: () => import('@/views/Inventory.vue'),  meta: { title: '库存管理' } },
      { path: 'inbound',    component: () => import('@/views/Inbound.vue'),    meta: { title: '入库管理' } },
      { path: 'outbound',   component: () => import('@/views/Outbound.vue'),   meta: { title: '出库管理' } },
      { path: 'stocktake',  component: () => import('@/views/Stocktake.vue'),  meta: { title: '库存盘点' } },
      { path: 'products',   component: () => import('@/views/Products.vue'),   meta: { title: '商品管理' } },
      { path: 'suppliers',  component: () => import('@/views/Suppliers.vue'),  meta: { title: '供应商管理' } },
      { path: 'logs',       component: () => import('@/views/Logs.vue'),       meta: { title: '操作日志' } },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })

NProgress.configure({ showSpinner: false })

router.beforeEach((to) => {
  NProgress.start()
  if (!getActivePinia()) return to.meta.public ? true : '/login'
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isLoggedIn) return '/login'
  if (to.path === '/login' && auth.isLoggedIn) return '/'
})

router.afterEach(() => NProgress.done())

export default router
