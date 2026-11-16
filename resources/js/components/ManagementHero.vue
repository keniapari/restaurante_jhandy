<script setup lang="ts">
import type { Component } from 'vue';

defineProps<{
    title: string;
    description: string;
    icon?: Component;
}>();
</script>

<template>
    <section
        class="relative overflow-hidden rounded-[2rem] border border-white/90 bg-white shadow-[0_22px_55px_-30px_rgba(6,78,59,0.45)] ring-1 ring-amber-200/60"
    >
        <img
            src="/images/restaurant/interior.jpg"
            alt="Interior del Restaurante Jhandy"
            class="absolute inset-0 h-full w-full object-cover object-right"
        />
        <div
            class="absolute inset-0 bg-gradient-to-r from-[#f7f2e7] via-[#f7f2e7]/92 to-transparent sm:via-[#f7f2e7]/80 lg:via-[#f7f2e7]/55"
        ></div>
        <div
            class="pointer-events-none absolute -bottom-20 left-1/3 size-52 rounded-full bg-amber-200/40 blur-3xl"
        ></div>
        <div
            class="relative flex min-h-40 flex-col items-start justify-between gap-5 p-5 sm:flex-row sm:items-center sm:p-7 lg:min-h-44"
        >
            <div class="flex max-w-2xl items-center gap-4 sm:gap-5">
                <div
                    class="flex size-16 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-emerald-900 via-emerald-700 to-amber-600 text-amber-50 shadow-xl shadow-emerald-900/25 sm:size-20"
                >
                    <slot name="icon">
                        <component
                            v-if="icon"
                            :is="icon"
                            class="size-8 sm:size-9"
                        />
                    </slot>
                </div>
                <div>
                    <h1
                        class="text-2xl font-black tracking-tight text-slate-950 sm:text-3xl"
                    >
                        {{ title }}
                    </h1>
                    <p
                        class="mt-1 max-w-xl text-sm text-slate-600 sm:text-base"
                    >
                        {{ description }}
                    </p>
                </div>
            </div>
            <div class="flex w-full flex-wrap items-center gap-2 sm:w-auto">
                <slot />
            </div>
        </div>
    </section>
</template>
