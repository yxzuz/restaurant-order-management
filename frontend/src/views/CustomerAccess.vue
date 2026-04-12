<template>
  <div class="min-h-screen bg-background">
    <section class="relative overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(251,146,60,0.2),_transparent_40%),linear-gradient(180deg,_rgba(255,247,237,1),_rgba(255,255,255,1))]">
      <div class="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
        <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_360px]">
          <div class="rounded-[2rem] border border-white/80 bg-white/85 p-8 shadow-sm backdrop-blur">
            <p class="text-sm font-semibold uppercase tracking-[0.3em] text-orange-600">
              Customer ordering
            </p>
            <h1 class="mt-4 font-heading text-4xl font-bold text-foreground sm:text-5xl">
              Scan your table QR code to start ordering.
            </h1>
            <p class="mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
              Each table QR code opens a secure ordering session for that table. If you already have the QR link, paste it below and continue.
            </p>

            <div class="mt-8 grid gap-4 sm:grid-cols-3">
              <div class="rounded-2xl border border-border bg-background p-4">
                <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 1</p>
                <p class="mt-2 font-medium text-foreground">Open your camera</p>
              </div>
              <div class="rounded-2xl border border-border bg-background p-4">
                <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 2</p>
                <p class="mt-2 font-medium text-foreground">Scan the table QR code</p>
              </div>
              <div class="rounded-2xl border border-border bg-background p-4">
                <p class="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 3</p>
                <p class="mt-2 font-medium text-foreground">Review menu and place order</p>
              </div>
            </div>
          </div>

          <div class="rounded-[2rem] border border-border bg-card p-6 shadow-sm">
            <p class="text-xs font-semibold uppercase tracking-[0.24em] text-orange-600">Already have the link?</p>
            <h2 class="mt-2 text-2xl font-semibold text-foreground">Open table session</h2>
            <p class="mt-2 text-sm leading-6 text-muted-foreground">
              Paste the full QR link here. Example format: `/table/5?token=...`
            </p>

            <label class="mt-6 block text-sm font-medium text-foreground" for="qr-link">
              QR link
            </label>
            <input
              id="qr-link"
              v-model.trim="qrLink"
              type="text"
              placeholder="http://localhost:5173/table/5?token=..."
              class="mt-2 w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
              @keydown.enter="openQrLink"
            >

            <p
              v-if="errorMessage"
              class="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {{ errorMessage }}
            </p>

            <button
              type="button"
              class="mt-6 flex w-full items-center justify-center rounded-2xl bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
              @click="openQrLink"
            >
              Open ordering page
            </button>

            <button
              type="button"
              class="mt-3 flex w-full items-center justify-center rounded-2xl border border-border px-4 py-3 text-sm font-medium text-foreground transition hover:bg-accent"
              @click="router.push('/')"
            >
              Back to home
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const qrLink = ref('')
const errorMessage = ref('')

function openQrLink() {
  errorMessage.value = ''

  if (!qrLink.value) {
    errorMessage.value = 'Paste the table QR link first.'
    return
  }

  try {
    const parsedUrl = qrLink.value.startsWith('http')
      ? new URL(qrLink.value)
      : new URL(qrLink.value, window.location.origin)

    if (!parsedUrl.pathname.startsWith('/table/')) {
      errorMessage.value = 'That link does not point to a table ordering page.'
      return
    }

    if (!parsedUrl.searchParams.get('token')) {
      errorMessage.value = 'The QR link is missing its table token.'
      return
    }

    router.push(`${parsedUrl.pathname}${parsedUrl.search}`)
  } catch {
    errorMessage.value = 'That QR link is not valid.'
  }
}
</script>
