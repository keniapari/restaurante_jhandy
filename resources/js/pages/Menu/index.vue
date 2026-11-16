<script setup lang="ts">
import { Head, Link } from '@inertiajs/vue3';
import { Minus, Plus, Search, ShoppingBag, UtensilsCrossed } from 'lucide-vue-next';
import { computed, ref } from 'vue';
import ManagementHero from '@/components/ManagementHero.vue';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useMenuOrder } from '@/composables/useMenuOrder';
import { conformar, index } from '@/routes/menu';
import type { Plato } from '@/types';

const props = defineProps<{
    platos: Plato[];
    categorias: string[];
}>();

const { totalItems, subtotal, cantidadDe, addItem, updateCantidad } =
    useMenuOrder();

const search = ref('');

const platosFiltrados = computed(() => {
    const term = search.value.trim().toLowerCase();

    if (!term) {
        return props.platos;
    }

    return props.platos.filter(
        (plato) =>
            plato.nombre.toLowerCase().includes(term) ||
            (plato.descripcion ?? '').toLowerCase().includes(term) ||
            plato.categoria.toLowerCase().includes(term),
    );
});

const categoriasConPlatos = computed(() =>
    props.categorias
        .map((categoria) => ({
            categoria,
            platos: platosFiltrados.value.filter(
                (plato) => plato.categoria === categoria,
            ),
        }))
        .filter((grupo) => grupo.platos.length > 0),
);

function formatCurrency(value: number): string {
    return new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(value);
}

defineOptions({
    layout: {
        breadcrumbs: [
            {
                title: 'Menú',
                href: index(),
            },
        ],
    },
});
</script>

<template>
    <Head title="Menú" />

    <div
        class="flex h-full flex-1 flex-col gap-5 rounded-xl bg-gradient-to-br from-emerald-200 via-amber-100 to-teal-200 p-4"
    >
        <ManagementHero
            title="Menú del Restaurante"
            description="Explora los platos disponibles y arma el pedido de tus clientes."
        >
            <template #icon><UtensilsCrossed class="h-7 w-7" /></template>
            <Button as-child :disabled="totalItems === 0">
                <Link :href="conformar().url">
                    <ShoppingBag class="mr-2 h-4 w-4" />
                    Conformar pedido
                    <Badge v-if="totalItems > 0" class="ml-2" variant="secondary">
                        {{ totalItems }}
                    </Badge>
                </Link>
            </Button>
        </ManagementHero>

        <div
            class="flex items-center gap-2 rounded-xl border border-emerald-300 bg-gradient-to-r from-amber-200/90 via-emerald-100/90 to-teal-200/90 p-4 shadow-md"
        >
            <div class="relative max-w-sm flex-1">
                <Search
                    class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                />
                <Input
                    v-model="search"
                    placeholder="Buscar platos por nombre o categoría..."
                    class="pl-10"
                />
            </div>
        </div>

        <div v-if="categoriasConPlatos.length === 0" class="rounded-2xl border border-emerald-300 bg-white/70 p-12 text-center text-sm text-muted-foreground">
            <UtensilsCrossed class="mx-auto mb-2 h-8 w-8 opacity-40" />
            No hay platos disponibles con ese criterio.
        </div>

        <section
            v-for="grupo in categoriasConPlatos"
            :key="grupo.categoria"
            class="space-y-3"
        >
            <div class="flex items-center gap-2">
                <h2 class="text-lg font-semibold text-emerald-900">
                    {{ grupo.categoria }}
                </h2>
                <Badge variant="secondary">{{ grupo.platos.length }}</Badge>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <article
                    v-for="plato in grupo.platos"
                    :key="plato.id"
                    class="flex flex-col overflow-hidden rounded-2xl border border-emerald-300 bg-white/85 shadow-md transition-shadow hover:shadow-xl"
                >
                    <img
                        :src="plato.imagen ?? '/images/restaurant/plato-1.jpg'"
                        :alt="plato.nombre"
                        class="h-40 w-full object-cover"
                    />
                    <div class="flex flex-1 flex-col gap-3 p-4">
                        <div class="flex items-start justify-between gap-2">
                            <h3 class="font-semibold text-emerald-950">
                                {{ plato.nombre }}
                            </h3>
                            <span class="whitespace-nowrap font-semibold text-emerald-700">
                                {{ formatCurrency(Number(plato.precio)) }}
                            </span>
                        </div>
                        <p class="line-clamp-2 flex-1 text-xs text-muted-foreground">
                            {{ plato.descripcion ?? 'Sin descripción.' }}
                        </p>

                        <div class="flex items-center justify-between">
                            <div v-if="cantidadDe(plato.id) > 0" class="flex items-center gap-2">
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    @click="updateCantidad(plato.id, cantidadDe(plato.id) - 1)"
                                >
                                    <Minus class="h-4 w-4" />
                                </Button>
                                <span class="w-6 text-center text-sm font-semibold">
                                    {{ cantidadDe(plato.id) }}
                                </span>
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    @click="updateCantidad(plato.id, cantidadDe(plato.id) + 1)"
                                >
                                    <Plus class="h-4 w-4" />
                                </Button>
                            </div>
                            <Button v-else size="sm" @click="addItem(plato)">
                                <Plus class="mr-1 h-4 w-4" />
                                Agregar
                            </Button>
                        </div>
                    </div>
                </article>
            </div>
        </section>

        <div
            v-if="totalItems > 0"
            class="sticky bottom-4 flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-gradient-to-r from-emerald-900 to-emerald-800 px-5 py-4 text-amber-50 shadow-2xl"
        >
            <div class="flex items-center gap-3">
                <ShoppingBag class="h-5 w-5 text-amber-200" />
                <p class="text-sm">
                    <span class="font-semibold">{{ totalItems }}</span>
                    {{ totalItems === 1 ? 'plato seleccionado' : 'platos seleccionados' }}
                    · Total: <span class="font-semibold">{{ formatCurrency(subtotal) }}</span>
                </p>
            </div>
            <Button as-child variant="secondary">
                <Link :href="conformar().url">
                    Conformar pedido
                </Link>
            </Button>
        </div>
    </div>
</template>
