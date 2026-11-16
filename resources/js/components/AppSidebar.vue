<script setup lang="ts">
import { Link } from '@inertiajs/vue3';
import {
    BarChart3,
    BookOpen,
    CalendarDays,
    ChefHat,
    ClipboardList,
    CreditCard,
    LayoutGrid,
    Shield,
    ShoppingBag,
    User,
    UtensilsCrossed,
} from 'lucide-vue-next';
import { computed } from 'vue';
import AppLogo from '@/components/AppLogo.vue';
import NavMain from '@/components/NavMain.vue';
import NavUser from '@/components/NavUser.vue';
import {
    Sidebar,
    SidebarContent,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from '@/components/ui/sidebar';
import { useCurrentUrl } from '@/composables/useCurrentUrl';
import { usePermissions } from '@/composables/usePermissions';
import { dashboard } from '@/routes';
import { index as clienteMenuIndex } from '@/routes/cliente/menu';
import { edit as pagosEdit } from '@/routes/configuracion/pagos';
import { index as pedidosIndex } from '@/routes/gestion/pedidos';
import { conformar as conformarIndex, index as menuIndex } from '@/routes/menu';
import { index as platosIndex } from '@/routes/platos';
import { index as reportesIndex } from '@/routes/reportes';
import { index as reservasIndex } from '@/routes/reservas';
import type { NavItem } from '@/types';

const { can, hasRole } = usePermissions();
const { isCurrentUrl } = useCurrentUrl();

const esCliente = computed(() => hasRole('cliente'));
const dashboardUrl = dashboard().url;
const homeUrl = computed(() =>
    esCliente.value ? clienteMenuIndex().url : dashboardUrl,
);

const mainNavItems = computed<NavItem[]>(() => {
    if (esCliente.value) {
        return [
            {
                title: 'Nuestra Carta',
                href: clienteMenuIndex().url,
                icon: UtensilsCrossed,
            },
            {
                title: 'Mi Perfil',
                href: '/perfil',
                icon: User,
            },
        ];
    }

    const items: {
        title: string;
        href: string;
        permission?: string;
        hiddenForVendedor?: boolean;
        adminOnly?: boolean;
        icon: any;
    }[] = [
        {
            title: 'Dashboard',
            href: dashboardUrl,
            permission: 'panel.ver',
            icon: LayoutGrid,
        },
        {
            title: 'Pedidos',
            href: pedidosIndex().url,
            permission: 'pedidos.ver',
            icon: ClipboardList,
        },
        {
            title: 'Menú',
            href: menuIndex().url,
            permission: 'menu.ver',
            icon: UtensilsCrossed,
        },
        {
            title: 'Conformar pedido',
            href: conformarIndex().url,
            permission: 'pedidos.crear',
            icon: ShoppingBag,
        },
        {
            title: 'Registrar platos',
            href: platosIndex().url,
            permission: 'platos.ver',
            icon: ChefHat,
        },
        {
            title: 'Registrar reservas',
            href: reservasIndex().url,
            permission: 'reservas.ver',
            icon: CalendarDays,
        },
        {
            title: 'Reportes',
            href: reportesIndex().url,
            permission: 'reportes.ventas.ver',
            icon: BarChart3,
        },
        {
            title: 'Roles y Permisos',
            href: '/roles',
            permission: 'usuarios.gestion',
            icon: Shield,
        },
        {
            title: 'Usuarios',
            href: '/usuarios',
            permission: 'usuarios.gestion',
            icon: User,
        },
        {
            title: 'QR de transferencia',
            href: pagosEdit().url,
            adminOnly: true,
            icon: CreditCard,
        },
    ];

    return items.filter((item) => {
        if (item.adminOnly && !hasRole('admin')) {
            return false;
        }

        if (item.permission && !can(item.permission)) {
            return false;
        }

        return !(item.hiddenForVendedor && hasRole('vendedor'));
    });
});
</script>

<template>
    <Sidebar
        collapsible="offcanvas"
        class="sidebar-gradient-unified sticky top-0 z-10 h-svh"
    >
        <SidebarHeader>
            <SidebarMenu>
                <SidebarMenuItem>
                    <SidebarMenuButton size="lg" as-child>
                        <Link :href="homeUrl">
                            <AppLogo />
                        </Link>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarHeader>

        <SidebarContent class="flex flex-col gap-0">
            <NavMain :items="mainNavItems" />

            <div v-if="!esCliente" class="space-y-0.5 px-3 pt-1">
                <Link
                    :href="menuIndex().url"
                    prefetch="hover"
                    :data-active="isCurrentUrl(menuIndex().url)"
                    :class="[
                        'group/link flex items-center gap-3 rounded-lg px-4 py-2 text-sm font-semibold tracking-wide transition-all duration-200',
                        isCurrentUrl(menuIndex().url)
                            ? 'border border-emerald-900/10 bg-gradient-to-r from-emerald-900 to-emerald-800 text-amber-50 shadow-md'
                            : 'border border-transparent text-emerald-950/80 hover:bg-white hover:text-emerald-800 hover:shadow-md',
                    ]"
                >
                    <BookOpen
                        :class="[
                            'h-5 w-5 flex-shrink-0 transition-transform duration-200 group-hover/link:scale-110',
                            isCurrentUrl(menuIndex().url)
                                ? 'text-amber-200'
                                : 'text-emerald-700/50 group-hover/link:text-emerald-600',
                        ]"
                    />
                    <span class="truncate">Ver Menú</span>
                </Link>
            </div>

            <div class="mt-auto">
                <NavUser />
            </div>
        </SidebarContent>
    </Sidebar>
    <slot />
</template>

<style>
.sidebar-gradient-unified,
.sidebar-gradient-unified [data-sidebar='sidebar'] {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(231, 206, 142, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 100%,
            rgba(16, 185, 129, 0.22),
            transparent 40%
        ),
        linear-gradient(
            170deg,
            #0b3d2e 0%,
            #11503c 42%,
            #0a3327 72%,
            #08281f 100%
        ) !important;
    background-size: 300% 300% !important;
    animation: unified-gradient 26s ease infinite !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-right: 1px solid rgba(201, 162, 39, 0.35) !important;
    box-shadow: 18px 0 50px -30px rgba(6, 78, 59, 0.65) !important;
}

.sidebar-gradient-unified a,
.sidebar-gradient-unified button {
    color: #f8f4ec !important;
}

.sidebar-gradient-unified [data-sidebar='group-label'] {
    background: none !important;
    -webkit-text-fill-color: #e7ce8e !important;
    color: #e7ce8e !important;
}

.sidebar-gradient-unified svg {
    color: #e7ce8e !important;
}

.sidebar-gradient-unified a:hover,
.sidebar-gradient-unified button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #fff8e7 !important;
}

.sidebar-gradient-unified [data-active='true'] {
    background: linear-gradient(90deg, #c9a227, #e7ce8e) !important;
    color: #0b2a20 !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 10px 24px -10px rgba(201, 162, 39, 0.85) !important;
}

.sidebar-gradient-unified [data-active='true'] svg {
    color: #0b2a20 !important;
}

.sidebar-gradient-unified [data-sidebar='menu-button'] span,
.sidebar-gradient-unified [data-sidebar='sidebar'] span {
    color: inherit;
}

@keyframes unified-gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}
</style>
