<script setup lang="ts">
import { Link } from '@inertiajs/vue3';

const { title = '', description = '' } = defineProps<{
    title?: string;
    description?: string;
}>();
</script>

<template>
    <div
        class="auth-bg relative flex min-h-svh items-center justify-center overflow-hidden px-4 py-10 sm:px-6"
    >
        <div
            class="pointer-events-none absolute -top-32 -left-24 size-80 rounded-full bg-amber-300/30 blur-3xl"
        ></div>
        <div
            class="pointer-events-none absolute -right-24 bottom-0 size-96 rounded-full bg-emerald-400/20 blur-3xl"
        ></div>

        <div
            class="relative grid w-full max-w-5xl overflow-hidden rounded-[2rem] border border-amber-200/70 bg-white/90 shadow-[0_40px_90px_-40px_rgba(6,78,59,0.55)] ring-1 ring-white/70 backdrop-blur-xl lg:grid-cols-[1.05fr_0.95fr]"
        >
            <div
                class="h-1.5 w-full bg-gradient-to-r from-emerald-900 via-amber-500 to-emerald-900 lg:col-span-2"
            ></div>

            <aside class="relative hidden lg:block">
                <img
                    src="/images/restaurant/interior.jpg"
                    alt="Interior de Restaurante Jhandy"
                    class="absolute inset-0 h-full w-full object-cover"
                />
                <div
                    class="absolute inset-0 bg-gradient-to-t from-[#06130f] via-[#0b3d2e]/80 to-[#0b3d2e]/25"
                ></div>
                <div
                    class="relative flex h-full flex-col justify-between p-10 text-amber-50"
                >
                    <Link href="/" class="flex items-center gap-3">
                        <img
                            src="/images/restaurant/logo.svg"
                            alt="Logo de Restaurante Jhandy"
                            class="size-11 rounded-full ring-2 ring-amber-300/60"
                        />
                        <span class="text-lg font-semibold tracking-tight">
                            Restaurante Jhandy
                        </span>
                    </Link>

                    <div class="space-y-4">
                        <span
                            class="inline-flex items-center gap-2 rounded-full border border-amber-300/40 bg-amber-300/15 px-3 py-1 text-xs font-semibold tracking-wide text-amber-200 uppercase"
                        >
                            Cocina de autor
                        </span>
                        <h2
                            class="font-serif text-4xl leading-tight font-semibold text-amber-50"
                        >
                            Cada servicio,<br />una experiencia.
                        </h2>
                        <p
                            class="max-w-xs text-sm leading-relaxed text-amber-100/80"
                        >
                            Gestiona pedidos, inventario y clientes con la
                            elegancia de nuestra cocina.
                        </p>
                        <div class="flex gap-2 pt-2">
                            <span
                                class="h-1.5 w-10 rounded-full bg-amber-300"
                            ></span>
                            <span
                                class="h-1.5 w-10 rounded-full bg-amber-200/50"
                            ></span>
                            <span
                                class="h-1.5 w-10 rounded-full bg-amber-200/50"
                            ></span>
                        </div>
                    </div>
                </div>
            </aside>

            <main class="flex flex-col justify-center p-6 sm:p-10">
                <div
                    class="mb-8 flex items-center justify-center gap-3 lg:hidden"
                >
                    <img
                        src="/images/restaurant/logo.svg"
                        alt="Logo de Restaurante Jhandy"
                        class="size-11 rounded-full ring-2 ring-amber-300/60"
                    />
                    <span class="text-lg font-bold text-[#0b3d2e]">
                        Restaurante Jhandy
                    </span>
                </div>

                <div class="mx-auto w-full max-w-sm">
                    <div class="mb-6 space-y-1.5 text-center lg:text-left">
                        <span
                            class="inline-flex items-center gap-2 rounded-full border border-amber-300/70 bg-amber-100/70 px-3 py-1 text-[11px] font-bold tracking-widest text-amber-800 uppercase"
                        >
                            Acceso al sistema
                        </span>
                        <h1
                            class="pt-1 text-2xl font-bold tracking-tight text-[#0b3d2e]"
                        >
                            {{ title }}
                        </h1>
                        <p class="text-sm leading-relaxed text-[#0b3d2e]/65">
                            {{ description }}
                        </p>
                    </div>

                    <slot />

                    <p
                        class="mt-8 text-center text-xs tracking-wide text-[#0b3d2e]/45"
                    >
                        © {{ new Date().getFullYear() }} Restaurante Jhandy
                    </p>
                </div>
            </main>
        </div>
    </div>
</template>

<style scoped>
.auth-bg {
    background:
        radial-gradient(
            circle at 12% 10%,
            rgba(201, 162, 39, 0.28),
            transparent 42%
        ),
        radial-gradient(
            circle at 88% 15%,
            rgba(16, 185, 129, 0.24),
            transparent 40%
        ),
        radial-gradient(
            circle at 70% 95%,
            rgba(20, 99, 74, 0.18),
            transparent 45%
        ),
        linear-gradient(135deg, #f7efdd 0%, #eaf3ec 55%, #f8f1de 100%);
}
</style>
