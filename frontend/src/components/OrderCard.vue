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
          </div>

          <div class="mt-3 flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
            <span>{{ formattedTime }}</span>
            <span class="h-1 w-1 rounded-full bg-border" />
            <span>{{ timeAgo }}</span>
          </div>
        </div>

        <div class="text-left sm:text-right">
          <p class="text-xs font-medium uppercase tracking-[0.2em] text-muted-foreground">Total</p>
          <p class="mt-1 text-2xl font-semibold text-orange-600">${{ totalAmount }}</p>
        </div>
      </div>

      <div class="mt-4 space-y-2">
        <p class="text-sm font-semibold text-foreground">Items</p>
        <div class="space-y-2">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="flex items-center justify-between rounded-2xl bg-muted/50 px-3 py-2"
          >
            <div class="min-w-0">
              <p class="truncate text-sm font-medium text-foreground">
                {{ item.menu_item?.name || 'Menu item' }}
              </p>
              <p class="text-xs text-muted-foreground">Qty {{ item.quantity }}</p>
            </div>
            <p class="text-sm font-semibold text-foreground">${{ Number(item.subtotal).toFixed(2) }}</p>
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
          v-if="nextStatusAction"
          type="button"
          class="rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:opacity-90"
          @click="$emit('advance-status', order)"
        >
          {{ nextStatusAction }}
        </button>
        <span
          v-if="order.status === 'Completed'"
          class="rounded-xl border border-border bg-muted px-4 py-2 text-sm font-medium text-muted-foreground"
        >
          Order Complete
        </span>
        <span
          v-if="order.status === 'Cancelled'"
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

const props = defineProps({
  order: {
    type: Object,
    required: true,
  },
})

defineEmits(['advance-status', 'cancel-order'])

const totalAmount = computed(() => Number(props.order.total_amount).toFixed(2))
const canCancel = computed(() => props.order.status === 'New')

const formattedTime = computed(() => {
  const createdAt = new Date(props.order.created_at)
  if (Number.isNaN(createdAt.getTime())) {
    return 'Unknown time'
  }

  return createdAt.toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})

const nextStatusAction = computed(() => {
  const statusActions = {
    New: 'Mark Preparing',
    Preparing: 'Mark Ready',
    Ready: 'Mark Complete',
  }

  return statusActions[props.order.status] || ''
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
