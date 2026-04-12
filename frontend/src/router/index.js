import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/owner/dashboard',
    component: () => import('@/views/OwnerDashboard.vue'),
    meta: { requiresAuth: true, requiredRole: 'owner' },
  },
  {
    path: '/owner/menu',
    component: () => import('@/views/OwnerMenu.vue'),
    meta: { requiresAuth: true, requiredRole: 'owner' },
  },
  {
    path: '/owner/orders',
    component: () => import('@/views/OwnerOrder.vue'),
    meta: { requiresAuth: true, requiredRole: 'owner' },
  },
  {
    path: '/owner/staff',
    component: () => import('@/views/OwnerStaff.vue'),
    meta: { requiresAuth: true, requiredRole: 'owner' },
  },
  {
    path: '/owner/analytics',
    component: () => import('@/views/OwnerAnalytics.vue'),
    meta: { requiresAuth: true, requiredRole: 'owner' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (!to.meta.requiresAuth) {
    return true
  }

  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('user_role')

  if (!token) {
    localStorage.removeItem('user_role')
    return '/'
  }

  if (to.meta.requiredRole && userRole !== to.meta.requiredRole) {
    localStorage.removeItem('token')
    localStorage.removeItem('user_role')
    return '/'
  }

  return true
})

export default router
