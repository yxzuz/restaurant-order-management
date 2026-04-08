<template>
  <aside
    class="flex h-screen shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-all duration-200"
    :class="collapsed ? 'w-20' : 'w-72'"
  >
    <div class="flex items-center justify-between border-b border-sidebar-border px-4 py-4">
      <div v-if="!collapsed" class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
          <UtensilsCrossed class="h-5 w-5" />
        </div>
        <div>
          <p class="font-heading text-lg font-bold text-sidebar-primary">OrderFlow</p>

        </div>
      </div>
      <button
        type="button"
        class="rounded-xl border border-sidebar-border p-2 text-muted-foreground transition hover:bg-sidebar-accent"
        @click="$emit('toggle')"
      >
        <PanelLeftClose v-if="!collapsed" class="h-4 w-4" />
        <PanelLeftOpen v-else class="h-4 w-4" />
      </button>
    </div>

    <!-- <div class="px-4 py-4" v-if="!collapsed">
      <p class="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">
        {{ role === 'owner' ? 'Owner Portal' : 'Staff Portal' }}
      </p>
    </div> -->

    <nav class="flex-1 space-y-1 px-3">
      <router-link
        v-for="item in items"
        :key="item.title"
        :to="item.url"
        class="flex items-center gap-3 rounded-2xl px-3 py-3 text-sm font-medium transition-colors"
        :class="isActive(item.url)
          ? 'bg-sidebar-accent/20 text-sidebar-primary ring-1 ring-sidebar-accent/25'
          : 'text-muted-foreground hover:bg-sidebar-accent/10 hover:text-sidebar-primary'"
      >
        <component :is="item.icon" class="h-5 w-5 shrink-0" />
        <span v-if="!collapsed">{{ item.title }}</span>
      </router-link>
    </nav>

    <div class="border-t border-sidebar-border p-3">
      <button
        @click="logout"
        class="flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-sm font-medium text-muted-foreground transition hover:bg-sidebar-accent hover:text-sidebar-primary"
      >
        <LogOut class="h-5 w-5 shrink-0" />
        <span v-if="!collapsed">Exit</span>
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
  LogOut,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-vue-next'

const props = defineProps({
  role: {
    type: String,
    default: 'owner',
  },
  collapsed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle'])

const route = useRoute()
const router = useRouter()

const staffItems = [
  { title: 'Orders', url: '/staff/orders', icon: ClipboardList },
]

const ownerItems = [
  { title: 'Dashboard', url: '/owner/dashboard', icon: LayoutDashboard },
  { title: 'Orders', url: '/owner/orders', icon: ClipboardList },
  { title: 'Menu', url: '/owner/menu', icon: UtensilsCrossed },
  { title: 'Analytics', url: '/owner/analytics', icon: BarChart3 },
]

const items = computed(() => {
  return props.role === 'owner' ? ownerItems : staffItems
})

function isActive(path) {
  return route.path.startsWith(path)
}

function logout() {
  localStorage.removeItem('token')
  router.push('/')
}
</script>
