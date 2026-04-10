<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="font-heading text-3xl font-bold text-foreground">Order Management</h1>
          <p class="mt-1 text-sm text-muted-foreground">Track live kitchen progress and table orders</p>
        </div>
      </div>

      <div class="grid gap-4">
        <OrderCard
          v-for="order in orders"
          :key="order.id"
          :order="order"
          @advance-status="advanceStatus"
          @cancel-order="cancelOrder"
        />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'

import DashboardLayout from '@/components/DashboardLayout.vue'
import OrderCard from '@/components/OrderCard.vue'
import { mockOrders } from '@/data/mock-data'

const orders = ref(mockOrders.map((order) => ({ ...order, items: order.items.map((item) => ({ ...item })) })))

const nextStatusMap = {
  New: 'Preparing',
  Preparing: 'Ready',
  Ready: 'Completed',
}

function advanceStatus(order) {
  const nextStatus = nextStatusMap[order.status]
  if (!nextStatus) {
    return
  }

  orders.value = orders.value.map((currentOrder) =>
    currentOrder.id === order.id
      ? { ...currentOrder, status: nextStatus }
      : currentOrder
  )
}

function cancelOrder(order) {
  if (order.status !== 'New') {
    return
  }

  orders.value = orders.value.map((currentOrder) =>
    currentOrder.id === order.id
      ? { ...currentOrder, status: 'Cancelled' }
      : currentOrder
  )
}
</script>
