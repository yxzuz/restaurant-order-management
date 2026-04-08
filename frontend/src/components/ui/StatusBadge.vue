<template>
  <span
    class="inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium"
    :class="statusClasses"
  >
    {{ status }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
  },
})

const stylesByStatus = {
  New: 'border-info/30 bg-info/10 text-info',
  Preparing: 'border-warning/30 bg-warning/10 text-amber-700',
  Ready: 'border-success/30 bg-success/10 text-success',
  Completed: 'border-border bg-muted text-muted-foreground',
  Cancelled: 'border-destructive/30 bg-destructive/10 text-destructive',
}

const statusClasses = computed(() => {
  return stylesByStatus[props.status] || 'border-border bg-muted text-muted-foreground'
})
</script>
