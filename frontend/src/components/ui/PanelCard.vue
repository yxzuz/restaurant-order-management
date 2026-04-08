<template>
  <section class="rounded-2xl border border-border bg-card shadow-sm">
    <header class="border-b border-border px-5 py-4">
      <h2 class="font-heading text-lg font-bold text-foreground">{{ title }}</h2>
      <p v-if="subtitle" class="mt-1 text-sm text-muted-foreground">{{ subtitle }}</p>
    </header>
    <div class="px-5 py-4">
      <slot />
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})
</script>
