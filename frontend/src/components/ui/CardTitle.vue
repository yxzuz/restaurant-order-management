<template>
  <component :is="as" :class="classes">
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  as: {
    type: String,
    default: 'h3',
  },
  class: {
    type: String,
    default: '',
  },
})

const classes = computed(() => cn('text-2xl font-semibold leading-none tracking-tight', props.class))
</script>
