<template>
  <article class="overflow-hidden rounded-3xl border border-border bg-card shadow-sm">
    <div class="p-5">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <p class="rounded-full bg-accent px-3 py-1 text-sm font-semibold text-foreground">
              Table {{ order.table_number }}
            </p>
            <StatusBadge :status="order.status" />
            <span 
              v-if="isPaid" 
              class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700"
            >
              Paid
            </span>
            <span 
              v-else 
              class="rounded-full bg-orange-100 px-3 py-1 text-xs font-semibold text-orange-700"
            >
              Unpaid
            </span>
          </div>

          <div class="mt-3 flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
            <span>{{ formattedTime }}</span>
            <span class="h-1 w-1 rounded-full bg-border" />
            <span>{{ timeAgo }}</span>
          </div>
        </div>

        <div class="text-left sm:text-right">
          <p class="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Total</p>
          <p class="mt-1 text-2xl font-semibold text-orange-600">{{ formatCurrency(order.total_amount) }}</p>
        </div>
      </div>

      <div class="mt-4 space-y-2">
        <p class="text-sm font-semibold text-foreground">Items</p>
        <div class="space-y-2">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="flex flex-col gap-2 rounded-2xl bg-muted/50 px-3 py-2"
          >
            <div class="flex items-center justify-between">
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2">
                  <p class="truncate text-sm font-medium text-foreground">
                    {{ item.menu_item?.name || 'Menu item' }}
                  </p>
                  <StatusBadge :status="item.status || 'new'" />
                </div>
                <p class="text-xs text-muted-foreground">Qty {{ item.quantity }}</p>
              </div>
              <p class="text-sm font-semibold text-foreground">{{ formatCurrency(getOrderItemSubtotal(item)) }}</p>
            </div>
            <div class="flex gap-2">
              <button
                v-if="getNextItemAction(item)"
                type="button"
                class="flex-1 rounded-lg bg-primary/10 px-3 py-1.5 text-xs font-semibold text-primary transition hover:bg-primary/20"
                @click="$emit('advance-item-status', order, item)"
              >
                {{ getNextItemAction(item) }}
              </button>
              <button
                v-if="canCancelItem(item)"
                type="button"
                class="rounded-lg border border-destructive/30 px-3 py-1.5 text-xs font-semibold text-destructive transition hover:bg-destructive/10"
                @click="$emit('cancel-item', order, item)"
              >
                ✕ Cancel
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-5 flex flex-wrap justify-end gap-3">
        <button
          v-if="canCancel"
          type="button"
          class="rounded-xl border border-destructive/30 px-4 py-2 text-sm font-semibold text-destructive transition hover:bg-destructive/10"
          @click="$emit('cancel-order', order)"
        >
          Cancel Order
        </button>
        <button
          v-if="canMarkPaid"
          type="button"
          class="rounded-xl bg-green-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-green-700"
          @click="$emit('mark-paid', order)"
        >
          💵 Mark as Paid
        </button>
        <span
          v-if="!canMarkPaid && !isPaid && allItemsCompleted"
          class="rounded-xl border border-orange-200 bg-orange-50 px-4 py-2 text-sm font-medium text-orange-700"
        >
          All items ready - waiting for payment
        </span>
        <span
          v-if="!allItemsCompleted && !isPaid"
          class="rounded-xl border border-border bg-muted px-4 py-2 text-sm font-medium text-muted-foreground"
        >
          {{ incompleteItemsCount }} item{{ incompleteItemsCount === 1 ? '' : 's' }} in progress
        </span>
        <span
          v-if="isPaid"
          class="rounded-xl border border-green-200 bg-green-50 px-4 py-2 text-sm font-medium text-green-700"
        >
          ✓ Paid & Complete
        </span>
        <span
          v-if="normalizedStatus === 'cancelled'"
          class="rounded-xl border border-destructive/20 bg-destructive/10 px-4 py-2 text-sm font-medium text-destructive"
        >
          Order Cancelled
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

import StatusBadge from '@/components/ui/StatusBadge.vue'
import { getOrderItemSubtotal } from '@/services/owner'

const props = defineProps({
  order: {
    type: Object,
    required: true,
  },
})

defineEmits(['advance-status', 'cancel-order', 'mark-paid', 'advance-item-status', 'cancel-item'])

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(value)
}

const normalizedStatus = computed(() => String(props.order.status || '').toLowerCase())
const normalizedPaymentStatus = computed(() => String(props.order.payment_status || props.order.paymentStatus || 'unpaid').toLowerCase())
const isPaid = computed(() => normalizedPaymentStatus.value === 'paid')
const canCancel = computed(() => normalizedStatus.value === 'new')

const allItemsCompleted = computed(() => {
  if (!props.order.items || props.order.items.length === 0) return false
  return props.order.items.every(item => 
    String(item.status || 'new').toLowerCase() === 'completed'
  )
})

const incompleteItemsCount = computed(() => {
  if (!props.order.items) return 0
  return props.order.items.filter(item => 
    String(item.status || 'new').toLowerCase() !== 'completed'
  ).length
})

const canMarkPaid = computed(() => {
  return !isPaid.value && 
         normalizedStatus.value !== 'cancelled' && 
         allItemsCompleted.value
})

const getNextItemAction = (item) => {
  const itemStatus = String(item.status || 'new').toLowerCase()
  const itemStatusActions = {
    new: '→ Start Preparing',
    preparing: '→ Mark Ready',
    ready: '→ Mark Complete',
  }
  return itemStatusActions[itemStatus] || ''
}

const canCancelItem = (item) => {
  const itemStatus = String(item.status || 'new').toLowerCase()
  return !isPaid.value && itemStatus === 'new'
}

const formattedTime = computed(() => {
  const createdAt = new Date(props.order.created_at)
  if (Number.isNaN(createdAt.getTime())) {
    return 'Unknown time'
  }

  return createdAt.toLocaleString('en-US', {
    timeZone: 'Asia/Bangkok',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  })
})

const timeAgo = computed(() => {
  const createdAt = new Date(props.order.created_at)
  const diffMs = Date.now() - createdAt.getTime()

  if (Number.isNaN(createdAt.getTime()) || diffMs < 0) {
    return 'Just now'
  }

  const diffMinutes = Math.floor(diffMs / 60000)
  if (diffMinutes < 1) {
    return 'Just now'
  }
  if (diffMinutes < 60) {
    return `${diffMinutes} minute${diffMinutes === 1 ? '' : 's'} ago`
  }

  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) {
    return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
  }

  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`
})
</script>
