<template>
  <div class="flex min-h-screen bg-gray-100">

    <!-- Sidebar -->
    <AppSidebar role="owner" />

    <!-- Right content -->
    <div class="flex-1 p-6">
      <slot />
    </div>

  </div>
</template>

<script setup>
import AppSidebar from '@/components/AppSidebar.vue'
</script>