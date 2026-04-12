<template>
  <div
    class="overflow-hidden rounded-2xl border border-border bg-card shadow-sm transition hover:shadow-lg"
    :class="{ 'opacity-60': !item.is_available }"
  >
    <div class="aspect-video overflow-hidden bg-muted">
      <img
        :src="item.image_url || fallbackImage"
        :alt="item.name"
        class="h-full w-full object-cover"
      >
    </div>

    <div class="space-y-4 p-4">
      <div>
        <div class="flex items-center gap-2 flex-wrap">
          <h3 class="font-heading text-lg font-semibold text-foreground">
            {{ item.name }}
          </h3>
          <span :class="categoryBadgeClass">
            {{ item.category }}
          </span>
          <span
            v-if="!item.is_available"
            class="rounded-full bg-destructive/10 px-2 py-0.5 text-xs font-medium text-destructive"
          >
            Unavailable
          </span>
        </div>

        <p class="mt-2 text-sm text-muted-foreground leading-relaxed">
          {{ item.description }}
        </p>
      </div>

      <div class="flex items-center justify-between border-t border-border pt-3">
        <div>
          <p class="text-lg font-semibold text-foreground">฿{{ item.price }}</p>
        </div>

        <div
          v-if="item.is_available"
          class="flex items-center gap-2"
        >
          <button
            v-if="quantity > 0"
            type="button"
            @click="$emit('remove', item)"
            class="flex h-9 w-9 items-center justify-center rounded-full border border-border text-foreground transition hover:bg-accent"
          >
            <Minus class="h-4 w-4" />
          </button>

          <span
            v-if="quantity > 0"
            class="min-w-6 text-center text-sm font-semibold text-foreground"
          >
            {{ quantity }}
          </span>

          <button
            type="button"
            @click="$emit('add', item)"
            class="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground transition hover:bg-primary/90"
          >
            <Plus class="h-4 w-4" />
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
