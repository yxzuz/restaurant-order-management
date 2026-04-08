<template>
  <div :class="classes">
    <slot />
  </div>
</template>

<script setup>
import { computed, provide, ref, watch } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  defaultValue: {
    type: String,
    default: '',
  },
  class: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
const currentValue = ref(props.modelValue || props.defaultValue)

watch(
  () => props.modelValue,
  (value) => {
    if (value !== undefined && value !== currentValue.value) {
      currentValue.value = value
    }
  },
)

function setValue(value) {
  currentValue.value = value
  emit('update:modelValue', value)
}

provide('tabsValue', currentValue)
provide('setTabsValue', setValue)

const classes = computed(() => cn(props.class))
</script>
