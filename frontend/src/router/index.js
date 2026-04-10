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
  component: () => import('@/views/OwnerDashboard.vue')
  },
  {
    path: '/owner/menu',
    component: () => import('@/views/OwnerMenu.vue')
  },
  {
    path: '/owner/orders',
    component: () => import('@/views/OwnerOrder.vue')
  },
  {
    path: '/owner/analytics',
    component: () => import('@/views/OwnerAnalytics.vue')
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
