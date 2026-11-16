<script setup lang="ts">
import { Head, Link, usePage } from '@inertiajs/vue3';
import {
    BarChart3,
    CalendarDays,
    ChefHat,
    ClipboardList,
    Sparkles,
    UserRound,
    Users,
    UtensilsCrossed,
} from 'lucide-vue-next';
import { computed } from 'vue';
import { usePermissions } from '@/composables/usePermissions';
import { dashboard } from '@/routes';
import { conformar, index as menu } from '@/routes/menu';
import { index as platos } from '@/routes/platos';
import { index as reportes } from '@/routes/reportes';
import { index as reservas } from '@/routes/reservas';

const props = defineProps<{
    stats: {
        totalUsuarios: number;
        totalClientes: number;
        totalPlatos: number;
        platosDisponibles: number;
        totalPedidos: number;
        pedidosPendientes: number;
        pedidosHoy: number;
        ventasHoy: number;
        ventasMes: number;
        totalReservas: number;
        reservasPendientes: number;
    };
    isVendedor: boolean;
}>();

const page = usePage();
const { can } = usePermissions();

const user = computed(() => page.props.auth?.user ?? null);
const userRoles = computed(() => page.props.auth?.roles ?? []);

function capitalizeName(name: string): string {
    return name.replace(/\b\w/g, (char) => char.toUpperCase());
}

const roleInfo = computed(() => {
    const roles = userRoles.value;

    if (roles.includes('admin')) {
        return {
            greeting: 'Bienvenida',
            title: 'Panel administrativo del restaurante',
            roleName: 'Administradora',
        };
    }

    if (roles.includes('vendedor')) {
        return {
            greeting: 'Bienvenida',
            title: 'Pedidos, menú y reservas del día',
            roleName: 'Vendedor',
        };
    }

    if (roles.includes('encargado_inventario')) {
        return {
            greeting: 'Bienvenida',
            title: 'Cocina y disponibilidad de platos',
            roleName: 'Encargado de cocina',
        };
    }

    return {
        greeting: 'Bienvenido',
        title: 'Panel de control',
        roleName: 'Usuario',
    };
});

const userName = computed(() => {
    const name = user.value?.name;

    return name ? capitalizeName(name) : 'Usuario';
});

const userInitial = computed(() => userName.value.charAt(0).toUpperCase());

defineOptions({
    layout: {
        breadcrumbs: [
            {
                title: 'Dashboard',
                href: dashboard(),
            },
        ],
    },
});

const cards = computed(() => [
    {
        title: 'Usuarios',
        value: props.stats.totalUsuarios,
        icon: Users,
        gradient: 'from-emerald-50 via-white to-emerald-100',
        iconColor: 'text-emerald-700',
        bar: 'bg-emerald-600',
    },
    {
        title: 'Clientes',
        value: props.stats.totalClientes,
        icon: UserRound,
        gradient: 'from-rose-50 via-white to-rose-100',
        iconColor: 'text-rose-600',
        bar: 'bg-rose-500',
    },
    {
        title: 'Pedidos',
        value: props.stats.totalPedidos,
        icon: ClipboardList,
        gradient: 'from-amber-50 via-white to-amber-100',
        iconColor: 'text-amber-700',
        bar: 'bg-amber-500',
    },
    {
        title: 'Platos',
        value: props.stats.totalPlatos,
        icon: ChefHat,
        gradient: 'from-teal-50 via-white to-teal-100',
        iconColor: 'text-teal-700',
        bar: 'bg-teal-600',
    },
    {
        title: 'Reservas',
        value: props.stats.totalReservas,
        icon: CalendarDays,
        gradient: 'from-fuchsia-50 via-white to-fuchsia-100',
        iconColor: 'text-fuchsia-700',
        bar: 'bg-fuchsia-500',
    },
]);

const summaries = computed(() => [
    {
        label: 'Pedidos de hoy',
        value: props.stats.pedidosHoy,
        hint: `${props.stats.pedidosPendientes} pendientes de atención`,
    },
    {
        label: 'Reservas pendientes',
        value: props.stats.reservasPendientes,
        hint: 'Por confirmar o asignar mesa',
    },
    {
        label: 'Ingresos de hoy',
        value: `Bs. ${props.stats.ventasHoy.toFixed(2)}`,
        hint: `Bs. ${props.stats.ventasMes.toFixed(2)} en el mes`,
    },
    {
        label: 'Platos disponibles',
        value: props.stats.platosDisponibles,
        hint: `de ${props.stats.totalPlatos} registrados`,
    },
]);

const quickLinks = computed(() =>
    [
        {
            title: 'Ver menú',
            description: 'Catálogo de platos disponibles',
            href: menu().url,
            icon: UtensilsCrossed,
            permission: 'menu.ver',
        },
        {
            title: 'Conformar pedido',
            description: 'Registrar un pedido de mesa o para llevar',
            href: conformar().url,
            icon: ClipboardList,
            permission: 'pedidos.gestion',
        },
        {
            title: 'Registrar platos',
            description: 'Administrar el menú del restaurante',
            href: platos().url,
            icon: ChefHat,
            permission: 'platos.ver',
        },
        {
            title: 'Reservas',
            description: 'Gestionar las reservas de los clientes',
            href: reservas().url,
            icon: CalendarDays,
            permission: 'reservas.ver',
        },
        {
            title: 'Reportes',
            description: 'Consultar reportes de ventas y compras',
            href: reportes().url,
            icon: BarChart3,
            permission: 'reportes.ventas.ver',
        },
    ].filter((link) => can(link.permission)),
);
</script>

<template>
    <Head title="Dashboard" />

    <div
        class="flex h-full flex-1 flex-col gap-6 overflow-x-auto bg-gradient-to-br from-amber-50/60 via-white to-emerald-50/60 p-6 lg:p-8"
    >
        <section
            class="relative overflow-hidden rounded-3xl border border-white/70 bg-gradient-to-br from-emerald-900 via-emerald-800 to-emerald-700 p-6 text-amber-50 shadow-xl shadow-emerald-900/20 sm:p-8"
        >
            <div
                class="pointer-events-none absolute -top-16 -right-10 h-56 w-56 rounded-full bg-amber-400/20 blur-3xl"
            />
            <div
                class="pointer-events-none absolute -bottom-20 left-1/3 h-48 w-48 rounded-full bg-emerald-300/20 blur-3xl"
            />

            <div
                class="relative flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between"
            >
                <div class="flex items-center gap-4">
                    <div
                        class="flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-100/15 text-2xl font-bold text-amber-200 ring-1 ring-amber-200/30"
                    >
                        {{ userInitial }}
                    </div>
                    <div>
                        <p
                            class="flex items-center gap-2 text-sm font-medium text-amber-200"
                        >
                            <Sparkles class="h-4 w-4" />
                            {{ roleInfo.greeting }}, {{ roleInfo.roleName }}
                        </p>
                        <h1 class="mt-1 text-2xl font-bold sm:text-3xl">
                            {{ userName }}
                        </h1>
                        <p class="mt-1 text-sm text-emerald-100/80">
                            {{ roleInfo.title }}
                        </p>
                    </div>
                </div>

                <div
                    class="grid grid-cols-2 gap-3 text-center sm:grid-cols-2 sm:text-right"
                >
                    <div class="rounded-2xl bg-white/10 px-4 py-3">
                        <p class="text-xs text-amber-200">Pedidos pendientes</p>
                        <p class="text-xl font-bold">
                            {{ props.stats.pedidosPendientes }}
                        </p>
                    </div>
                    <div class="rounded-2xl bg-white/10 px-4 py-3">
                        <p class="text-xs text-amber-200">Reservas pendientes</p>
                        <p class="text-xl font-bold">
                            {{ props.stats.reservasPendientes }}
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
            <div
                v-for="card in cards"
                :key="card.title"
                class="relative overflow-hidden rounded-2xl border border-white/80 bg-gradient-to-br p-5 shadow-md shadow-slate-200/60"
                :class="card.gradient"
            >
                <div class="flex items-start justify-between gap-3">
                    <div>
                        <p
                            class="text-xs font-semibold tracking-wide text-slate-500 uppercase"
                        >
                            {{ card.title }}
                        </p>
                        <p class="mt-2 text-3xl font-bold text-slate-800">
                            {{ card.value }}
                        </p>
                    </div>
                    <div class="rounded-xl bg-white/80 p-2 shadow-sm">
                        <component
                            :is="card.icon"
                            class="h-5 w-5"
                            :class="card.iconColor"
                        />
                    </div>
                </div>
                <span
                    class="absolute inset-x-4 bottom-0 h-1 rounded-full opacity-70"
                    :class="card.bar"
                />
            </div>
        </div>

        <div class="grid gap-6 lg:grid-cols-2">
            <section
                class="rounded-2xl border border-emerald-100 bg-white/85 p-6 shadow-md shadow-slate-200/50 backdrop-blur"
            >
                <h2 class="text-lg font-semibold text-slate-800">
                    Resumen del día
                </h2>
                <p class="mt-1 text-sm text-slate-500">
                    Estado general de la operación del restaurante.
                </p>

                <div class="mt-5 grid gap-3 sm:grid-cols-2">
                    <div
                        v-for="item in summaries"
                        :key="item.label"
                        class="rounded-xl border border-slate-100 bg-slate-50/70 p-4"
                    >
                        <p class="text-xs font-medium text-slate-500">
                            {{ item.label }}
                        </p>
                        <p class="mt-1 text-2xl font-bold text-slate-800">
                            {{ item.value }}
                        </p>
                        <p class="mt-1 text-xs text-slate-400">
                            {{ item.hint }}
                        </p>
                    </div>
                </div>
            </section>

            <section
                class="rounded-2xl border border-emerald-100 bg-white/85 p-6 shadow-md shadow-slate-200/50 backdrop-blur"
            >
                <h2 class="text-lg font-semibold text-slate-800">
                    Accesos rápidos
                </h2>
                <p class="mt-1 text-sm text-slate-500">
                    Atajos a las tareas más frecuentes.
                </p>

                <div class="mt-5 space-y-2">
                    <Link
                        v-for="link in quickLinks"
                        :key="link.title"
                        :href="link.href"
                        class="flex items-center gap-4 rounded-xl border border-slate-100 bg-white p-3 transition-all hover:-translate-y-0.5 hover:border-emerald-200 hover:bg-emerald-50/60 hover:shadow-sm"
                    >
                        <span
                            class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-100"
                        >
                            <component
                                :is="link.icon"
                                class="h-5 w-5 text-emerald-700"
                            />
                        </span>
                        <span class="min-w-0">
                            <span
                                class="block text-sm font-semibold text-slate-800"
                            >
                                {{ link.title }}
                            </span>
                            <span class="block text-xs text-slate-500">
                                {{ link.description }}
                            </span>
                        </span>
                    </Link>
                </div>
            </section>
        </div>
    </div>
</template>
