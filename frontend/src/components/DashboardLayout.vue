<template>
  <div class="flex h-screen bg-background">
    <!-- Mobile Overlay -->
    <div
      v-if="sidebarOpen && !sidebarCollapsed"
      class="fixed inset-0 z-40 bg-black/50 lg:hidden"
      @click="closeSidebar"
    />

    <!-- Sidebar -->
    <AppSidebar
      :role="role"
      :collapsed="sidebarCollapsed"
      :mobile-open="sidebarOpen"
      @toggle="toggleSidebar"
      @close="closeSidebar"
    />

    <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
      <header class="flex h-14 md:h-16 shrink-0 items-center justify-between border-b border-border bg-card px-3 md:px-6">
        <!-- Mobile Menu Button -->
        <button
          class="lg:hidden rounded-lg p-2 hover:bg-accent"
          @click="openSidebar"
          type="button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="4" x2="20" y1="12" y2="12"/>
            <line x1="4" x2="20" y1="6" y2="6"/>
            <line x1="4" x2="20" y1="18" y2="18"/>
          </svg>
        </button>

        <div class="lg:block hidden">
          <p class="text-xs font-medium uppercase tracking-[0.25em] text-muted-foreground">
            {{ role === 'owner' ? 'Owner Portal' : 'Staff Portal' }}
          </p>
          <p class="mt-1 text-sm text-foreground">
            <span v-if="restaurantName" class="font-semibold">{{ restaurantName }}</span>
            <span v-else>Restaurant order operations</span>
          </p>
        </div>

        <!-- Mobile Title -->
        <div class="lg:hidden">
          <p class="text-sm font-semibold text-foreground">
            {{ restaurantName || 'Restaurant' }}
          </p>
        </div>

        <div />
      </header>

      <main class="flex-1 overflow-auto p-3 sm:p-4 md:p-6 lg:p-8">
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
const sidebarOpen = ref(false)
const restaurantName = ref('')

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

function openSidebar() {
  sidebarOpen.value = true
}

function closeSidebar() {
  sidebarOpen.value = false
}

onMounted(() => {
  restaurantName.value = localStorage.getItem('restaurant_name') || ''
})
</script>
