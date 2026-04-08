<template>
  <div :class="classes">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps({
  class: {
    type: String,
    default: '',
  },
})

const classes = computed(() =>
  cn('rounded-lg border bg-card text-card-foreground shadow-sm', props.class),
)
</script>
