<template>
  <DashboardLayout :role="userRole">
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
          @mark-paid="markOrderPaid"
          @advance-item-status="advanceItemStatus"
          @cancel-item="cancelItem"
        />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import DashboardLayout from '@/components/DashboardLayout.vue'
import OrderCard from '@/components/OrderCard.vue'
import { fetchOwnerOrders, updateOrderStatus, updateOrderPayment, updateOrderItemStatus, cancelOrderItem } from '@/services/owner'

const route = useRoute()

const orders = ref([])
const loading = ref(false)
const errorMessage = ref('')

// Determine role from route path
const userRole = computed(() => {
  if (route.path.startsWith('/staff')) return 'staff'
  if (route.path.startsWith('/owner')) return 'owner'
  return localStorage.getItem('user_role') || 'owner'
})

const nextStatusMap = {
  new: 'preparing',
  preparing: 'ready',
  ready: 'completed',
}

const nextItemStatusMap = {
  new: 'PREPARING',
  preparing: 'READY',
  ready: 'COMPLETED',
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

async function markOrderPaid(order) {
  errorMessage.value = ''

  try {
    const updatedOrder = await updateOrderPayment(order.id, 'paid')
    // Remove from active orders list since it's now closed
    orders.value = orders.value.filter(o => o.id !== order.id)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not mark order as paid.'
  }
}

async function advanceItemStatus(order, item) {
  const currentStatus = String(item.status || 'new').toLowerCase()
  const nextStatus = nextItemStatusMap[currentStatus]
  
  if (!nextStatus) {
    return
  }

  errorMessage.value = ''

  try {
    const updatedOrder = await updateOrderItemStatus(order.id, item.id, nextStatus)
    upsertOrder(updatedOrder)
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not update item status.'
  }
}

async function cancelItem(order, item) {
  errorMessage.value = ''

  try {
    const updatedOrder = await cancelOrderItem(order.id, item.id)
    
    // If order was cancelled (no items left), remove from list
    if (updatedOrder.status === 'CANCELLED' || updatedOrder.status === 'cancelled') {
      orders.value = orders.value.filter(o => o.id !== order.id)
    } else {
      // Otherwise just update the order
      upsertOrder(updatedOrder)
    }
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Could not cancel item.'
  }
}

function upsertOrder(updatedOrder) {
  orders.value = orders.value.map((currentOrder) =>
    currentOrder.id === updatedOrder.id ? updatedOrder : currentOrder
  )
}
</script>
