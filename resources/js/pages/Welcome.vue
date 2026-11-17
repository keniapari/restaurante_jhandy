<script setup lang="ts">
import { Head, Link, usePage } from '@inertiajs/vue3';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { login } from '@/routes';
import type { Plato } from '@/types';

const props = withDefaults(
    defineProps<{
        platos: Plato[];
        categorias: string[];
    }>(),
    {
        platos: () => [],
        categorias: () => [],
    },
);

const page = usePage();
const isScrolled = ref(false);
const platosComida = computed(() =>
    (props.platos ?? []).filter((p) => p.categoria !== 'Postres'),
);
const handleScroll = () => {
    isScrolled.value = window.scrollY > 20;
};
onMounted(() => window.addEventListener('scroll', handleScroll));
onUnmounted(() => window.removeEventListener('scroll', handleScroll));

const formatCurrency = (value: number): string =>
    new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(value);
</script>

<template>
    <Head title="Restaurante Jhandy - Nuestra Carta">
        <link rel="preconnect" href="https://rsms.me/" />
        <link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
    </Head>

    <div class="min-h-screen bg-stone-50 font-sans text-stone-900">
        <!-- Navbar -->
        <header
            :class="[
                'fixed top-0 right-0 left-0 z-50 transition-all duration-300',
                isScrolled
                    ? 'border-b border-stone-200/60 bg-white/80 shadow-sm backdrop-blur-xl'
                    : 'bg-transparent',
            ]"
        >
            <div
                class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8"
            >
                <Link href="/" class="flex items-center gap-2.5">
                    <img
                        src="/images/restaurant/logo.svg"
                        alt="Restaurante Jhandy"
                        class="h-9 w-9"
                    />
                    <span
                        class="text-lg font-bold tracking-tight text-emerald-800"
                    >
                        Restaurante Jhandy
                    </span>
                </Link>
                <nav class="flex items-center gap-3">
                    <template v-if="page.props.auth.user">
                        <Link
                            href="/dashboard"
                            class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-amber-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-emerald-200/40 transition-all hover:scale-[1.02] hover:shadow-xl"
                        >
                            Panel
                        </Link>
                    </template>
                    <template v-else>
                        <Link
                            :href="login().url"
                            class="rounded-lg px-4 py-2 text-sm font-semibold text-stone-600 transition-all hover:bg-emerald-50 hover:text-emerald-700"
                        >
                            Iniciar sesión
                        </Link>
                    </template>
                </nav>
            </div>
        </header>

        <!-- Hero -->
        <section class="relative overflow-hidden pt-24 pb-20 sm:pt-32 sm:pb-28">
            <div class="absolute inset-0 z-0">
                <img
                    src="/images/restaurant/interior.jpg"
                    alt="Restaurante Jhandy"
                    class="h-full w-full scale-105 object-cover animate-[kenburns_24s_ease-in-out_infinite]"
                />
                <div
                    class="absolute inset-0 bg-gradient-to-br from-emerald-950/80 via-stone-900/50 to-amber-900/70"
                ></div>
                <div
                    class="absolute inset-0 bg-gradient-to-t from-stone-900/40 via-transparent to-transparent"
                ></div>
            </div>
            <div
                class="pointer-events-none absolute top-[-200px] left-1/2 h-[900px] w-[900px] -translate-x-1/2 rounded-full bg-gradient-to-br from-emerald-400/15 to-amber-400/15 blur-3xl"
            ></div>

            <div
                class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"
            >
                <div
                    class="grid items-center gap-12 lg:grid-cols-2 lg:gap-16"
                >
                    <div class="text-center lg:text-left">
                        <div
                            class="mb-6 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-xs font-medium text-white/90 backdrop-blur-md shadow-sm"
                        >
                            <span
                                class="flex h-2 w-2 animate-pulse rounded-full bg-gradient-to-r from-emerald-400 to-amber-400"
                            ></span>
                            Cocina tradicional y moderna
                        </div>
                        <h1
                            class="mb-6 text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl"
                        >
                            Bienvenido a
                            <span class="inline-block">
                                <span
                                    v-for="(letra, i) in 'Restaurante Jhandy'.split('')"
                                    :key="i"
                                    class="inline-block text-amber-300 animate-[bounceLetter_1.2s_ease-in-out_infinite]"
                                    :style="{ animationDelay: i * 0.08 + 's' }"
                                >
                                    {{ letra === ' ' ? '\u00A0' : letra }}
                                </span>
                            </span>
                        </h1>
                        <p
                            class="mx-auto mb-10 max-w-2xl text-lg leading-relaxed text-white/80 sm:text-xl lg:mx-0"
                        >
                            Disfruta de nuestra carta con los mejores platos
                            tradicionales. Haz tu pedido en línea y paga por
                            transferencia de forma rápida y segura.
                        </p>
                        <div
                            class="flex flex-col items-center justify-center gap-4 sm:flex-row lg:justify-start"
                        >
                            <template v-if="!page.props.auth.user">
                                <Link
                                    :href="login().url"
                                    class="inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-amber-500 px-8 text-sm font-semibold text-white shadow-lg shadow-emerald-300/30 transition-all hover:scale-[1.02] hover:shadow-xl sm:w-auto"
                                >
                                    Iniciar sesión para pedir
                                    <svg
                                        class="h-4 w-4"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            d="M13 7l5 5m0 0l-5 5m5-5H6"
                                        />
                                    </svg>
                                </Link>
                            </template>
                            <template v-else>
                                <Link
                                    href="/carta"
                                    class="inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-amber-500 px-8 text-sm font-semibold text-white shadow-lg shadow-emerald-300/30 transition-all hover:scale-[1.02] hover:shadow-xl sm:w-auto"
                                >
                                    Ver mi carta
                                </Link>
                            </template>
                            <a
                                href="#menu"
                                class="inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl border border-white/30 bg-white/10 px-8 text-sm font-semibold text-white backdrop-blur-md transition-all hover:bg-white/20 sm:w-auto"
                            >
                                Ver menú
                            </a>
                        </div>
                    </div>
                    <div class="relative hidden lg:block">
                        <div
                            class="grid grid-cols-2 gap-4"
                        >
                            <div
                                class="relative col-span-2 overflow-hidden rounded-3xl shadow-2xl shadow-emerald-900/40"
                            >
                                <img
                                    src="/images/restaurant/plato-1.jpg"
                                    alt="Plato destacado"
                                    class="h-[320px] w-full object-cover animate-[kenburns_18s_ease-in-out_infinite]"
                                />
                                <div
                                    class="pointer-events-none absolute inset-0 bg-gradient-to-tr from-emerald-900/20 via-transparent to-amber-900/10"
                                ></div>
                            </div>
                            <div
                                class="overflow-hidden rounded-2xl shadow-xl shadow-emerald-900/30"
                            >
                                <img
                                    src="/images/restaurant/plato-4.jpg"
                                    alt="Plato"
                                    class="h-40 w-full object-cover transition-transform duration-500 hover:scale-105 animate-[float_6s_ease-in-out_infinite]"
                                />
                            </div>
                            <div
                                class="overflow-hidden rounded-2xl shadow-xl shadow-emerald-900/30"
                            >
                                <img
                                    src="/images/restaurant/plato-3.jpg"
                                    alt="Plato"
                                    class="h-40 w-full object-cover transition-transform duration-500 hover:scale-105 animate-[float_6s_ease-in-out_infinite]"
                                />
                            </div>
                        </div>
                        <div
                            class="pointer-events-none absolute -top-5 -right-5 h-24 w-24 rounded-3xl border border-white/30 bg-white/10 backdrop-blur-xl shadow-2xl"
                        ></div>
                        <div
                            class="pointer-events-none absolute -bottom-5 -left-5 h-20 w-20 rounded-2xl border border-white/20 bg-gradient-to-br from-emerald-200/20 to-amber-200/20 backdrop-blur-xl shadow-xl"
                        ></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Platos destacados -->
        <section id="menu" class="relative bg-white py-20 sm:py-28">
            <div
                class="pointer-events-none absolute top-0 left-0 h-[400px] w-[400px] rounded-full bg-gradient-to-tr from-emerald-100/40 to-amber-100/40 blur-3xl"
            ></div>
            <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="mx-auto mb-14 max-w-2xl text-center">
                    <div
                        class="mb-4 inline-flex items-center gap-2 rounded-full border border-emerald-200/60 bg-emerald-50 px-4 py-1.5 text-xs font-medium text-emerald-700"
                    >
                        Nuestra carta
                    </div>
                    <h2
                        class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl"
                    >
                        Platos que te
                        <span
                            class="bg-gradient-to-r from-emerald-600 to-amber-600 bg-clip-text text-transparent"
                        >
                            enamorarán
                        </span>
                    </h2>
                    <p class="text-lg text-stone-500">
                        Una selección de nuestros platos más populares.
                    </p>
                </div>

                <div
                    v-if="platosComida.length === 0"
                    class="rounded-2xl border border-dashed border-emerald-200 bg-emerald-50/40 p-12 text-center text-stone-500"
                >
                    Próximamente nuestra carta estará disponible.
                </div>
                <div v-else class="relative overflow-hidden">
                    <div
                        class="flex gap-6 animate-[marquee_40s_linear_infinite] hover:[animation-play-state:paused]"
                    >
                        <article
                            v-for="(plato, i) in [...platosComida, ...platosComida]"
                            :key="plato.id + '-' + i"
                            class="group w-80 shrink-0 overflow-hidden rounded-2xl border border-emerald-100 bg-white shadow-sm transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-emerald-100/40"
                        >
                            <div class="relative h-44 overflow-hidden">
                                <img
                                    :src="
                                        plato.imagen ??
                                        '/images/restaurant/plato-1.jpg'
                                    "
                                    :alt="plato.nombre"
                                    class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105 animate-[float_6s_ease-in-out_infinite]"
                                />
                                <div
                                    class="absolute top-3 left-3 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-emerald-700 shadow-sm backdrop-blur"
                                >
                                    {{ plato.categoria }}
                                </div>
                            </div>
                            <div class="space-y-2 p-5">
                                <div
                                    class="flex items-start justify-between gap-3"
                                >
                                    <h3
                                        class="font-semibold text-stone-900 animate-[slide_3s_ease-in-out_infinite]"
                                    >
                                        {{ plato.nombre }}
                                    </h3>
                                    <span
                                        class="font-bold text-emerald-700"
                                    >
                                        {{
                                            formatCurrency(
                                                Number(plato.precio),
                                            )
                                        }}
                                    </span>
                                </div>
                                <p
                                    v-if="plato.descripcion"
                                    class="line-clamp-2 text-sm text-stone-500"
                                >
                                    {{ plato.descripcion }}
                                </p>
                            </div>
                        </article>
                    </div>
                </div>

                <div class="mt-12 text-center">
                    <Link
                        :href="login().url"
                        class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-amber-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-200/40 transition-all hover:scale-[1.02] hover:shadow-xl"
                    >
                        Inicia sesión para hacer tu pedido
                        <svg
                            class="h-4 w-4"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M13 7l5 5m0 0l-5 5m5-5H6"
                            />
                        </svg>
                    </Link>
                </div>
            </div>
        </section>

        <!-- Viñetas / por qué -->
        <section
            class="relative border-t border-stone-200/60 bg-gradient-to-b from-stone-50 to-emerald-50/40 py-20 sm:py-28"
        >
            <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="mx-auto mb-14 max-w-2xl text-center">
                    <h2
                        class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl"
                    >
                        ¿Por qué elegirnos?
                    </h2>
                    <p class="text-lg text-stone-500">
                        Una experiencia gastronómica pensada para ti.
                    </p>
                </div>
                <div
                    class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
                >
                    <div
                        class="rounded-2xl border border-emerald-100 bg-white/80 p-7 shadow-sm backdrop-blur-sm transition-all hover:shadow-lg"
                    >
                        <div
                            class="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-100 to-amber-100 text-emerald-700"
                        >
                            <svg
                                class="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="1.5"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M12 6v6l4 2"
                                />
                            </svg>
                        </div>
                        <h3 class="mb-2 text-lg font-semibold">
                            Servicio rápido
                        </h3>
                        <p class="text-sm leading-relaxed text-stone-500">
                            Pedidos ágiles y atención personalizada para que
                            disfrutes sin esperas.
                        </p>
                    </div>
                    <div
                        class="rounded-2xl border border-emerald-100 bg-white/80 p-7 shadow-sm backdrop-blur-sm transition-all hover:shadow-lg"
                    >
                        <div
                            class="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-100 to-amber-100 text-emerald-700"
                        >
                            <svg
                                class="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="1.5"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
                                />
                            </svg>
                        </div>
                        <h3 class="mb-2 text-lg font-semibold">
                            Ingredientes frescos
                        </h3>
                        <p class="text-sm leading-relaxed text-stone-500">
                            Seleccionamos los mejores ingredientes para cada
                            plato de nuestra carta.
                        </p>
                    </div>
                    <div
                        class="rounded-2xl border border-emerald-100 bg-white/80 p-7 shadow-sm backdrop-blur-sm transition-all hover:shadow-lg"
                    >
                        <div
                            class="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-100 to-amber-100 text-emerald-700"
                        >
                            <svg
                                class="h-5 w-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="1.5"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V6.75c0-.621.504-1.125 1.125-1.125h.375m0 0V6"
                                />
                            </svg>
                        </div>
                        <h3 class="mb-2 text-lg font-semibold">
                            Pago por transferencia
                        </h3>
                        <p class="text-sm leading-relaxed text-stone-500">
                            Realiza tu pago de forma segura escaneando nuestro
                            código QR.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Contacto -->
        <section
            class="relative border-t border-stone-200/60 bg-stone-900 py-20 text-stone-100 sm:py-28"
        >
            <div
                class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(16,185,129,0.15),transparent_50%)]"
            ></div>
            <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div
                    class="grid gap-10 lg:grid-cols-2 lg:gap-16"
                >
                    <div>
                        <h2 class="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
                            Visítanos
                        </h2>
                        <p class="mb-8 text-stone-300">
                            Estamos para atenderte. Contáctanos o ven a
                            disfrutar de nuestra comida.
                        </p>
                        <ul class="space-y-4 text-stone-300">
                            <li class="flex items-start gap-3">
                                <svg
                                    class="mt-1 h-5 w-5 flex-shrink-0 text-emerald-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="1.5"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"
                                    />
                                </svg>
                                <span
                                    >Av. Principal #123, Ciudad</span
                                >
                            </li>
                            <li class="flex items-start gap-3">
                                <svg
                                    class="mt-1 h-5 w-5 flex-shrink-0 text-emerald-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="1.5"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"
                                    />
                                </svg>
                                <span>+591 70000000</span>
                            </li>
                            <li class="flex items-start gap-3">
                                <svg
                                    class="mt-1 h-5 w-5 flex-shrink-0 text-emerald-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="1.5"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <span>Lun - Dom: 11:00 - 22:00</span>
                            </li>
                            <li class="flex items-start gap-3">
                                <svg
                                    class="mt-1 h-5 w-5 flex-shrink-0 text-emerald-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="1.5"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
                                    />
                                </svg>
                                <span>contacto@restaurantejhandy.com</span>
                            </li>
                        </ul>
                    </div>
                    <div
                        class="overflow-hidden rounded-3xl border border-stone-700/50 bg-stone-800/50 p-2 shadow-2xl backdrop-blur"
                    >
                        <iframe
                            title="Mapa"
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3800!2d-66.15!3d-17.39!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTfCsDIzJzI0LjAiUyA2NsKwMDknMDAuMCJX!5e0!3m2!1ses!2sbo!4v1"
                            class="h-72 w-full rounded-2xl border-0"
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade"
                        ></iframe>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer
            class="border-t border-stone-200 bg-white py-10"
        >
            <div
                class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6 lg:px-8"
            >
                <div class="flex items-center gap-2.5">
                    <img
                        src="/images/restaurant/logo.svg"
                        alt="Restaurante Jhandy"
                        class="h-7 w-7"
                    />
                    <span
                        class="text-sm font-semibold text-emerald-800"
                    >
                        Restaurante Jhandy
                    </span>
                </div>
                <p class="text-sm text-stone-400">
                    &copy; {{ new Date().getFullYear() }} Restaurante Jhandy.
                    Todos los derechos reservados.
                </p>
            </div>
        </footer>
    </div>
</template>

<style>
@keyframes kenburns {
    0% {
        transform: scale(1) translate(0, 0);
    }
    50% {
        transform: scale(1.12) translate(-3%, -2%);
    }
    100% {
        transform: scale(1) translate(0, 0);
    }
}
@keyframes shimmer {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 200% 50%;
    }
}
@keyframes marquee {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}
@keyframes float {
    0%,
    100% {
        transform: translateY(0) scale(1);
    }
    50% {
        transform: translateY(-4px) scale(1.03);
    }
}
@keyframes slide {
    0%,
    100% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(3px);
    }
}
@keyframes bounceLetter {
    0%,
    100% {
        transform: translateY(0) scale(1);
    }
    50% {
        transform: translateY(-16px) scale(1.12);
    }
}
</style>
