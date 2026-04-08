<template>
  <button
    type="button"
    role="tab"
    :class="classes"
    :aria-selected="isActive"
    @click="setTabsValue(value)"
  >
    <slot />
  </button>
</template>

<script setup>
import { computed, inject } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps({
  value: {
    type: String,
    required: true,
  },
  class: {
    type: String,
    default: '',
  },
})

const tabsValue = inject('tabsValue')
const setTabsValue = inject('setTabsValue')

const isActive = computed(() => tabsValue?.value === props.value)

const classes = computed(() =>
  cn(
    'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
    isActive.value ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground',
    props.class,
  ),
)
</script>
