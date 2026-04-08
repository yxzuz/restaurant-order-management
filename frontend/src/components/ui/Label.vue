<template>
  <label :for="forId" :class="classes">
    <slot />
  </label>
</template>

<script setup>
import { computed } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps({
  forId: {
    type: String,
    default: '',
  },
  class: {
    type: String,
    default: '',
  },
})

const classes = computed(() =>
  cn('text-sm font-medium leading-none', props.class),
)
</script>
