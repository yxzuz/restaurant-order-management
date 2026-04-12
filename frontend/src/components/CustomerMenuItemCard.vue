<template>
  <div
    class="overflow-hidden rounded-2xl border border-border bg-card shadow-sm transition hover:shadow-lg"
    :class="{ 'opacity-60': !item.is_available }"
  >
    <div class="aspect-[4/3] overflow-hidden bg-muted">
      <img
        :src="item.image_url || fallbackImage"
        :alt="item.name"
        class="h-full w-full object-cover"
      >
    </div>

    <div class="space-y-4 p-4">
      <div>
        <div class="flex items-center gap-2">
          <h3 class="truncate font-heading text-lg font-semibold text-foreground">
            {{ item.name }}
          </h3>
          <span
            v-if="!item.is_available"
            class="rounded-full bg-destructive/10 px-2 py-0.5 text-xs font-medium text-destructive"
          >
            Unavailable
          </span>
        </div>

        <CardDescription class="mt-2 leading-6">
          {{ item.description }}
        </CardDescription>
      </div>

      <div class="flex items-center justify-between border-t border-border pt-3">
        <div>
          <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">{{ item.category }}</p>
          <p class="mt-1 text-lg font-semibold text-foreground">฿{{ item.price }}</p>
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
import { Minus, Plus } from 'lucide-vue-next'

import fallbackImage from '@/assets/hero-restaurant.jpg'
import CardDescription from '@/components/ui/CardDescription.vue'

defineProps({
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
</script>
