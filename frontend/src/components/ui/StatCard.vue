<template>
  <div class="rounded-2xl border border-border bg-card p-5 shadow-sm">
    <div class="flex items-start justify-between gap-3">
      <div class="min-w-0 flex-1">
        <p class="text-sm font-medium text-muted-foreground">{{ title }}</p>
        <p class="mt-3 whitespace-pre-line font-heading text-xl sm:text-2xl lg:text-3xl font-bold text-foreground break-words">{{ value }}</p>
        <p class="mt-1 text-xs text-muted-foreground">{{ description }}</p>
      </div>
      <div class="rounded-xl bg-secondary p-3 text-muted-foreground shrink-0">
        <component :is="icon" class="h-5 w-5" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  icon: {
    type: Object,
    required: true,
  },
})
</script>
