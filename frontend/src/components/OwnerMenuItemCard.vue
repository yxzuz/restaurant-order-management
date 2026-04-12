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
      <div class="space-y-3">
        <div class="flex items-start gap-3">
          <div class="min-w-0 flex-1">
            <h3 class="font-heading text-lg font-semibold leading-snug text-foreground">
              {{ item.name }}
            </h3>
          </div>

          <div class="flex shrink-0 items-center gap-2">
            <p class="rounded-full border border-border px-2 py-0.5 font-body text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
              {{ item.category }}
            </p>
            <button
              v-if="canEdit"
              type="button"
              @click="$emit('edit', item)"
              class="rounded-full border border-border p-2 text-foreground transition hover:bg-accent"
              aria-label="Edit menu item"
            >
              <Pencil class="h-4 w-4" />
            </button>

            <button
              v-if="canDelete"
              type="button"
              class="rounded-full border border-destructive/30 px-3 py-2 text-sm text-destructive transition hover:bg-destructive/10"
              @click="$emit('delete', item)"
            >
              <Trash class="h-4 w-4" />
            </button>
          </div>
        </div>

        <CardDescription class="leading-6">
          {{ item.description }}
        </CardDescription>
      </div>

      <div class="flex items-center justify-between border-t border-border pt-3">
        <div>
          <p class="mt-1 text-lg font-semibold text-foreground">${{ item.price }}</p>
        </div>

        <div class="flex items-center gap-2">
          <button
            type="button"
            class="inline-flex items-center gap-3 rounded-full px-3 py-2 text-sm font-medium text-foreground transition"
            @click="$emit('toggle-availability', item)"
          >
            <span>{{ item.is_available ? 'Available' : 'Disabled' }}</span>
            <span
              class="relative inline-flex h-7 w-12 items-center rounded-full transition-colors"
              :class="item.is_available ? 'bg-orange-500/80' : 'bg-muted'"
            >
              <span
                class="inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform"
                :class="item.is_available ? 'translate-x-6' : 'translate-x-1'"
              />
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Pencil, Trash } from 'lucide-vue-next'

import CardDescription from '@/components/ui/CardDescription.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  userRole: {
    type: String,
    default: 'owner',
  },
})

defineEmits(['edit', 'delete', 'toggle-availability'])

const canEdit = computed(() => props.userRole === 'owner')
const canDelete = computed(() => props.userRole === 'owner')

const fallbackImage = 'https://fakeimg.pl/600x400/ebebeb/999?font=bebas&text=No+Image'
</script>
