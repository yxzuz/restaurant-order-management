<template>
  <div
    class="overflow-hidden rounded-xl border border-border bg-card shadow-sm transition hover:shadow-lg"
    :class="{ 'opacity-60': !item.is_available }"
  >
    <div class="aspect-[3/2] overflow-hidden bg-muted">
      <img
        :src="item.image_url || fallbackImage"
        :alt="item.name"
        class="h-full w-full object-cover"
      >
    </div>

    <div class="space-y-2.5 p-3">
      <div>
        <div class="flex items-center gap-1.5 flex-wrap">
          <h3 class="font-heading text-base font-semibold text-foreground">
            {{ item.name }}
          </h3>
          <span :class="categoryBadgeClass">
            {{ item.category }}
          </span>
          <span
            v-if="!item.is_available"
            class="rounded-full bg-destructive/10 px-1.5 py-0.5 text-xs font-medium text-destructive"
          >
            Unavailable
          </span>
        </div>

        <p v-if="item.description" class="mt-1.5 text-xs text-muted-foreground leading-snug line-clamp-2">
          {{ item.description }}
        </p>
      </div>

      <div class="flex items-center justify-between border-t border-border pt-2.5">
        <div>
          <p class="text-base font-semibold text-foreground">{{ formatCurrency(item.price) }}</p>
        </div>

        <div
          v-if="item.is_available"
          class="flex items-center gap-1.5"
        >
          <button
            v-if="quantity > 0"
            type="button"
            @click="$emit('remove', item)"
            class="flex h-8 w-8 items-center justify-center rounded-full border border-border text-foreground transition hover:bg-accent"
          >
            <Minus class="h-3.5 w-3.5" />
          </button>

          <span
            v-if="quantity > 0"
            class="min-w-5 text-center text-sm font-semibold text-foreground"
          >
            {{ quantity }}
          </span>

          <button
            type="button"
            @click="$emit('add', item)"
            class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground transition hover:bg-primary/90"
          >
            <Plus class="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Minus, Plus } from 'lucide-vue-next'

import fallbackImage from '@/assets/hero-restaurant.jpg'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  quantity: {
    type: Number,
    default: 0,
  },
})

defineEmits(['add', 'remove'])

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'THB',
  }).format(value)
}

const categoryBadgeClass = computed(() => {
  const category = props.item.category?.toLowerCase() || ''
  const baseClass = 'rounded-full px-2.5 py-0.5 text-xs font-medium '
  
  if (category.includes('appetizer')) {
    return baseClass + 'bg-green-100 text-green-700'
  } else if (category.includes('main')) {
    return baseClass + 'bg-orange-100 text-orange-700'
  } else if (category.includes('dessert')) {
    return baseClass + 'bg-pink-100 text-pink-700'
  } else if (category.includes('drink')) {
    return baseClass + 'bg-blue-100 text-blue-700'
  }
  return baseClass + 'bg-gray-100 text-gray-700'
})
</script>
