<template>
  <div :class="classes" role="tablist">
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
  cn('inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground', props.class),
)
</script>
