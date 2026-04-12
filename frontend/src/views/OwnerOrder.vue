<template>
  <DashboardLayout role="owner">
    <div class="space-y-6">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="font-heading text-3xl font-bold text-foreground">Order Management</h1>
          <p class="mt-1 text-sm text-muted-foreground">Track live kitchen progress and table orders</p>
        </div>
      </div>

      <p
        v-if="errorMessage"
        class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ errorMessage }}
      </p>

      <p v-if="loading" class="text-sm text-muted-foreground">Loading orders...</p>

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
import { onMounted, ref } from 'vue'

import DashboardLayout from '@/components/DashboardLayout.vue'
import OrderCard from '@/components/OrderCard.vue'
import { fetchOwnerOrders, updateOrderStatus } from '@/services/owner'

const orders = ref([])
const loading = ref(false)
const errorMessage = ref('')

const nextStatusMap = {
  new: 'preparing',
  preparing: 'ready',
  ready: 'completed',
}

onMounted(() => {
  loadOrders()
})

async function loadOrders() {
  loading.value = true
  errorMessage.value = ''

  try {
    orders.value = await fetchOwnerOrders()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not load orders.'
  } finally {
    loading.value = false
  }
}

async function advanceStatus(order) {
  const nextStatus = nextStatusMap[String(order.status).toLowerCase()]
  if (!nextStatus) {
    return
  }

  errorMessage.value = ''

  try {
    const updatedOrder = await updateOrderStatus(order.id, nextStatus)
    upsertOrder(updatedOrder)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not update order status.'
  }
}

async function cancelOrder(order) {
  if (String(order.status).toLowerCase() !== 'new') {
    return
  }

  errorMessage.value = ''

  try {
    const updatedOrder = await updateOrderStatus(order.id, 'cancelled')
    upsertOrder(updatedOrder)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not cancel order.'
  }
}

function upsertOrder(updatedOrder) {
  orders.value = orders.value.map((currentOrder) =>
    currentOrder.id === updatedOrder.id ? updatedOrder : currentOrder
  )
}
</script>
