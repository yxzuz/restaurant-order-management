<template>
  <div class="flex h-screen bg-background">
    <AppSidebar :role="role" :collapsed="sidebarCollapsed" @toggle="toggleSidebar" />

    <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
      <header class="flex h-16 shrink-0 items-center justify-between border-b border-border bg-card px-4 md:px-6">
        <div>
          <p class="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">
            {{ role === 'owner' ? 'Owner Portal' : 'Staff Portal' }}
          </p>
          <p class="mt-1 text-sm text-foreground">
            <span v-if="restaurantName" class="font-semibold">{{ restaurantName }}</span>
            <span v-else>Restaurant order operations</span>
          </p>
        </div>
      </header>

      <main class="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import AppSidebar from '@/components/AppSidebar.vue'

defineProps({
  role: {
    type: String,
    default: 'owner',
  },
})

const sidebarCollapsed = ref(false)
const restaurantName = ref('')

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

onMounted(() => {
  restaurantName.value = localStorage.getItem('restaurant_name') || ''
})
</script>
