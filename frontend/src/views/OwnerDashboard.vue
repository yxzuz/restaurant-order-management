<template>
  <DashboardLayout>

    <!-- Title -->
    <div class="mb-6">
      <h1 class="font-heading text-2xl font-bold">Dashboard</h1>
      <p class="text-gray-500">Overview of today's operations</p>
    </div>

    <!-- Cards -->
    <div class="grid gap-4 md:grid-cols-4 mb-6">

      <div class="bg-white p-4 rounded-full shadow">
        <p class="text-sm text-gray-500">Total Revenue</p>
        <h2 class="text-xl font-bold">$191.87</h2>
      </div>

      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Active Orders</p>
        <h2 class="text-xl font-bold">3</h2>
      </div>

      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Total Orders</p>
        <h2 class="text-xl font-bold">4</h2>
      </div>

      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Menu Items</p>
        <h2 class="text-xl font-bold">11</h2>
      </div>

    </div>

    <!-- Bottom -->
    <div class="grid gap-4 md:grid-cols-2">

      <!-- Recent Orders -->
      <div class="bg-white p-4 rounded shadow">
        <h2 class="font-semibold mb-4">Recent Orders</h2>

        <div class="space-y-3">
          <div class="flex justify-between">
            <div>
              <p>Table 3</p>
              <p class="text-sm text-gray-500">2 items</p>
            </div>
            <div class="text-right">
              <p>$59.97</p>
              <p class="text-sm text-gray-500">New</p>
            </div>
          </div>
        </div>

      </div>

      <!-- Popular -->
      <div class="bg-white p-4 rounded shadow">
        <h2 class="font-semibold mb-4">Popular Items</h2>

        <div class="flex justify-between">
          <p>#1 Grilled Salmon</p>
          <p>$24.99</p>
        </div>

      </div>

    </div>

  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/DashboardLayout.vue'
</script>