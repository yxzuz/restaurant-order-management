<template>
  <div
    aria-hidden="true"
    :class="classes"
  />
</template>

<script setup>
import { computed } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps({
  orientation: {
    type: String,
    default: 'horizontal',
  },
  class: {
    type: String,
    default: '',
  },
})

const classes = computed(() =>
  cn(
    'shrink-0 bg-border',
    props.orientation === 'vertical' ? 'h-full w-px' : 'h-px w-full',
    props.class,
  ),
)
</script>
