<template>
  <aside class="bg-[#2a221d] text-white shadow-md w-64 h-screen flex flex-col">
    <!-- Logo -->
    <div class="p-4 font-bold text-lg border-b border-white/10 text-white">
      🍽 OrderFlow
    </div>

    <!-- Menu -->
    <nav class="flex-1 p-2 space-y-2">

      <router-link
        v-for="item in items"
        :key="item.title"
        :to="item.url"
        class="flex items-center gap-2 p-2 rounded text-white transition-colors hover:bg-orange-500/10 hover:text-orange-200"
        :class="{ 'bg-orange-500/20 text-orange-300': isActive(item.url) }"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span>{{ item.title }}</span>
      </router-link>

    </nav>

        <!-- Footer -->
    <div class="p-4 border-t border-white/10">
      <button
        @click="logout"
        class="flex items-center gap-2 w-full p-2 rounded text-white transition-colors hover:bg-orange-500/10 hover:text-orange-200">
        <LogOut class="w-5 h-5" />
        <span>Exit</span>
      </button>
    </div>
  </aside>
</template>


<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import {
  LayoutDashboard,
  ClipboardList,
  UtensilsCrossed,
  BarChart3,
  LogOut
} from 'lucide-vue-next'

// props
const props = defineProps({
  role: String
})

const route = useRoute()
const router = useRouter()

// menu items
const staffItems = [
  { title: 'Orders', url: '/staff/orders', icon: ClipboardList },
]

const ownerItems = [
  { title: 'Dashboard', url: '/owner/dashboard', icon: LayoutDashboard },
  { title: 'Orders', url: '/owner/orders', icon: ClipboardList },
  { title: 'Menu', url: '/owner/menu', icon: UtensilsCrossed },
  { title: 'Analytics', url: '/owner/analytics', icon: BarChart3 },
]

// computed items
const items = computed(() => {
  return props.role === 'owner' ? ownerItems : staffItems
})

// active route check
function isActive(path) {
  return route.path.startsWith(path)
}

// logout
function logout() {
  localStorage.removeItem('token')
  router.push('/')
}
</script>
