<template>
  <span
    class="inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium"
    :class="statusClasses"
  >
    {{ displayStatus }}
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
  new: 'border-info/30 bg-info/10 text-info',
  preparing: 'border-warning/30 bg-warning/10 text-amber-700',
  ready: 'border-success/30 bg-success/10 text-success',
  completed: 'border-border bg-muted text-muted-foreground',
  cancelled: 'border-destructive/30 bg-destructive/10 text-destructive',
}

const statusClasses = computed(() => {
  return stylesByStatus[normalizedStatus.value] || 'border-border bg-muted text-muted-foreground'
})

const normalizedStatus = computed(() => String(props.status || '').toLowerCase())

const displayStatus = computed(() => {
  return normalizedStatus.value
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
})
</script>
