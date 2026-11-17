<script setup lang="ts">
import { Head, Link, useForm, usePage } from '@inertiajs/vue3';
import {
    Minus,
    Plus,
    Search,
    ShoppingBag,
    Trash2,
    UserRound,
    UtensilsCrossed,
    Wallet,
} from 'lucide-vue-next';
import { computed, ref } from 'vue';
import InputError from '@/components/InputError.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { login } from '@/routes';
import { store as storePedido } from '@/routes/cliente/menu';
import type { Plato } from '@/types';

type OrderLine = {
    plato_id: number;
    nombre: string;
    precio: number;
    imagen: string | null;
    cantidad: number;
};

const props = defineProps<{
    platos: Plato[];
    categorias: string[];
    qrPagoUrl: string | null;
}>();

const page = usePage();
const isGuest = computed(() => !page.props.auth?.user);
const items = ref<OrderLine[]>([]);
const busqueda = ref('');
const categoriaActiva = ref('Todas');

const form = useForm({
    observaciones: '',
    platos: [] as { plato_id: number; cantidad: number }[],
});

const categorias = computed(() => ['Todas', ...props.categorias]);

const platosFiltrados = computed(() => {
    const termino = busqueda.value.trim().toLowerCase();

    return props.platos.filter((plato) => {
        const coincideCategoria =
            categoriaActiva.value === 'Todas' ||
            plato.categoria === categoriaActiva.value;
        const coincideBusqueda =
            termino === '' ||
            plato.nombre.toLowerCase().includes(termino) ||
            (plato.descripcion ?? '').toLowerCase().includes(termino);

        return coincideCategoria && coincideBusqueda;
    });
});

const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.cantidad, 0),
);

const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.precio * item.cantidad, 0),
);

function formatCurrency(value: number): string {
    return new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(value);
}

function cantidadDe(platoId: number): number {
    return items.value.find((item) => item.plato_id === platoId)?.cantidad ?? 0;
}

function addPlato(plato: Plato) {
    const existente = items.value.find((item) => item.plato_id === plato.id);

    if (existente) {
        existente.cantidad = Math.min(50, existente.cantidad + 1);

        return;
    }

    items.value.push({
        plato_id: plato.id,
        nombre: plato.nombre,
        precio: Number(plato.precio) || 0,
        imagen: plato.imagen,
        cantidad: 1,
    });
}

function updateCantidad(platoId: number, cantidad: number) {
    const item = items.value.find((linea) => linea.plato_id === platoId);

    if (!item) {
        return;
    }

    if (cantidad <= 0) {
        removeItem(platoId);

        return;
    }

    item.cantidad = Math.min(50, cantidad);
}

function removeItem(platoId: number) {
    items.value = items.value.filter((item) => item.plato_id !== platoId);
}

function submit() {
    if (items.value.length === 0) {
        return;
    }

    form.platos = items.value.map((item) => ({
        plato_id: item.plato_id,
        cantidad: item.cantidad,
    }));

    form.post(storePedido().url, {
        preserveScroll: true,
    });
}
</script>

<template>
    <Head title="Nuestra Carta" />

    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:py-10">
        <section
            class="mb-8 overflow-hidden rounded-3xl border border-emerald-200 bg-gradient-to-r from-emerald-900 via-emerald-800 to-amber-700 p-6 text-amber-50 shadow-xl sm:p-8"
        >
            <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <span
                        class="inline-flex items-center gap-2 rounded-full border border-amber-200/40 bg-white/10 px-3 py-1 text-xs font-semibold tracking-wide uppercase"
                    >
                        <UtensilsCrossed class="h-3.5 w-3.5" />
                        Restaurante Jhandy
                    </span>
                    <h1 class="mt-3 text-3xl font-bold sm:text-4xl">
                        Nuestra Carta
                    </h1>
                    <p class="mt-2 max-w-xl text-sm text-amber-50/80">
                        Elige tus platos, agrégalos al carrito y confirma tu
                        pedido con pago por transferencia.
                    </p>
                </div>
                <div
                    class="flex items-center gap-2 rounded-2xl border border-white/15 bg-white/10 px-4 py-3 text-sm"
                >
                    <UserRound class="h-4 w-4 text-amber-200" />
                    <span v-if="!isGuest">
                        Pedido a nombre de
                        <strong>{{ page.props.auth.user?.name }}</strong>
                    </span>
                    <span v-else>
                        <Link
                            :href="login().url"
                            class="font-semibold text-amber-200 underline"
                        >
                            Inicia sesión para hacer tu pedido
                        </Link>
                    </span>
                </div>
            </div>
        </section>

        <div class="grid gap-6 lg:grid-cols-3">
            <div class="space-y-5 lg:col-span-2">
                <div
                    class="flex flex-wrap items-center gap-2 rounded-2xl border border-emerald-200 bg-white/90 p-4 shadow-sm"
                >
                    <button
                        v-for="categoria in categorias"
                        :key="categoria"
                        type="button"
                        class="rounded-full border px-3 py-1.5 text-xs font-semibold transition"
                        :class="
                            categoriaActiva === categoria
                                ? 'border-emerald-700 bg-emerald-700 text-white'
                                : 'border-emerald-200 bg-white text-emerald-800 hover:border-emerald-500'
                        "
                        @click="categoriaActiva = categoria"
                    >
                        {{ categoria }}
                    </button>
                    <div class="relative ml-auto w-full sm:w-60">
                        <Search
                            class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                        />
                        <Input
                            v-model="busqueda"
                            placeholder="Buscar plato..."
                            class="h-9 pl-9"
                        />
                    </div>
                </div>

                <div
                    v-if="platosFiltrados.length === 0"
                    class="rounded-2xl border border-dashed border-emerald-300 bg-white/60 p-12 text-center text-sm text-muted-foreground"
                >
                    <UtensilsCrossed class="mx-auto mb-2 h-8 w-8 opacity-40" />
                    No hay platos disponibles con ese criterio.
                </div>

                <div v-else class="grid gap-4 sm:grid-cols-2">
                    <article
                        v-for="plato in platosFiltrados"
                        :key="plato.id"
                        class="overflow-hidden rounded-2xl border border-emerald-200 bg-white shadow-sm transition hover:shadow-md"
                    >
                        <img
                            :src="plato.imagen ?? '/images/restaurant/plato-1.jpg'"
                            :alt="plato.nombre"
                            class="h-40 w-full object-cover"
                        />
                        <div class="space-y-2 p-4">
                            <div class="flex items-start justify-between gap-3">
                                <div>
                                    <h2 class="font-semibold text-emerald-950">
                                        {{ plato.nombre }}
                                    </h2>
                                    <p class="text-xs text-muted-foreground">
                                        {{ plato.categoria }}
                                    </p>
                                </div>
                                <span class="font-bold text-emerald-800">
                                    {{ formatCurrency(Number(plato.precio)) }}
                                </span>
                            </div>
                            <p
                                v-if="plato.descripcion"
                                class="line-clamp-2 text-xs text-muted-foreground"
                            >
                                {{ plato.descripcion }}
                            </p>

                            <div class="flex items-center justify-end gap-2 pt-1">
                                <template v-if="cantidadDe(plato.id) > 0">
                                    <Button
                                        type="button"
                                        variant="outline"
                                        size="icon-sm"
                                        @click="
                                            updateCantidad(
                                                plato.id,
                                                cantidadDe(plato.id) - 1,
                                            )
                                        "
                                    >
                                        <Minus class="h-4 w-4" />
                                    </Button>
                                    <span class="w-6 text-center font-semibold">
                                        {{ cantidadDe(plato.id) }}
                                    </span>
                                    <Button
                                        type="button"
                                        variant="outline"
                                        size="icon-sm"
                                        @click="addPlato(plato)"
                                    >
                                        <Plus class="h-4 w-4" />
                                    </Button>
                                </template>
                                <Button
                                    v-else
                                    type="button"
                                    size="sm"
                                    @click="addPlato(plato)"
                                >
                                    <Plus class="mr-1 h-4 w-4" />
                                    Agregar al carrito
                                </Button>
                            </div>
                        </div>
                    </article>
                </div>
            </div>

            <aside class="lg:sticky lg:top-6 lg:self-start">
                <form
                    class="space-y-4 rounded-2xl border border-emerald-200 bg-white/95 p-5 shadow-xl"
                    @submit.prevent="submit"
                >
                    <div class="flex items-center gap-2">
                        <ShoppingBag class="h-5 w-5 text-emerald-700" />
                        <h2 class="text-base font-semibold text-emerald-950">
                            Mi carrito
                        </h2>
                        <span
                            class="ml-auto rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800"
                        >
                            {{ totalItems }}
                        </span>
                    </div>

                    <div
                        v-if="items.length === 0"
                        class="rounded-xl border border-dashed border-emerald-200 p-6 text-center text-sm text-muted-foreground"
                    >
                        Agrega platos de la carta para armar tu pedido.
                    </div>

                    <div v-else class="space-y-3">
                        <div
                            v-for="item in items"
                            :key="item.plato_id"
                            class="flex items-center gap-3 rounded-xl border border-emerald-100 bg-emerald-50/50 p-2"
                        >
                            <img
                                :src="item.imagen ?? '/images/restaurant/plato-1.jpg'"
                                :alt="item.nombre"
                                class="h-12 w-12 rounded-lg object-cover"
                            />
                            <div class="min-w-0 flex-1">
                                <p class="truncate text-sm font-semibold">
                                    {{ item.nombre }}
                                </p>
                                <p class="text-xs text-muted-foreground">
                                    {{ formatCurrency(item.precio * item.cantidad) }}
                                </p>
                            </div>
                            <div class="flex items-center gap-1">
                                <Button
                                    type="button"
                                    variant="outline"
                                    size="icon-sm"
                                    @click="
                                        updateCantidad(
                                            item.plato_id,
                                            item.cantidad - 1,
                                        )
                                    "
                                >
                                    <Minus class="h-3.5 w-3.5" />
                                </Button>
                                <span class="w-5 text-center text-sm font-semibold">
                                    {{ item.cantidad }}
                                </span>
                                <Button
                                    type="button"
                                    variant="outline"
                                    size="icon-sm"
                                    @click="
                                        updateCantidad(
                                            item.plato_id,
                                            item.cantidad + 1,
                                        )
                                    "
                                >
                                    <Plus class="h-3.5 w-3.5" />
                                </Button>
                                <Button
                                    type="button"
                                    variant="outline"
                                    size="icon-sm"
                                    class="border-red-200 text-red-500 hover:bg-red-50"
                                    @click="removeItem(item.plato_id)"
                                >
                                    <Trash2 class="h-3.5 w-3.5" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div class="grid gap-2">
                        <Label for="observaciones">Observaciones</Label>
                        <textarea
                            id="observaciones"
                            v-model="form.observaciones"
                            rows="2"
                            maxlength="500"
                            placeholder="Ej: sin cebolla, bien cocido..."
                            class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50"
                        />
                        <InputError :message="form.errors.observaciones" />
                    </div>

                    <div
                        class="flex items-center justify-between border-t border-emerald-100 pt-3"
                    >
                        <span class="font-semibold text-emerald-950">Total</span>
                        <span class="text-2xl font-bold text-emerald-900">
                            {{ formatCurrency(total) }}
                        </span>
                    </div>

                    <div
                        class="flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 p-3 text-xs text-amber-800"
                    >
                        <Wallet class="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <p>
                            El pago es únicamente por
                            <strong>transferencia bancaria</strong>. Tu pedido
                            quedará pendiente hasta que el restaurante verifique
                            el pago.
                        </p>
                    </div>

                    <div
                        v-if="qrPagoUrl"
                        class="space-y-3 rounded-xl border border-emerald-200 bg-emerald-50 p-4"
                    >
                        <div>
                            <h3 class="text-sm font-semibold text-emerald-950">
                                Paga por transferencia
                            </h3>
                            <p class="mt-1 text-xs text-emerald-800">
                                Escanea el QR para realizar el pago. Después,
                                sube tu comprobante desde Mi perfil, en Mis
                                pedidos.
                            </p>
                        </div>
                        <img
                            :src="qrPagoUrl"
                            alt="Código QR para pagar por transferencia"
                            class="mx-auto max-h-56 w-auto rounded-lg border border-emerald-100 bg-white object-contain p-2"
                        />
                    </div>
                    <p
                        v-else
                        class="rounded-xl border border-amber-200 bg-amber-50 p-3 text-xs text-amber-800"
                    >
                        El código QR de transferencia aún no está configurado.
                        Consulta los datos de pago en el restaurante.
                    </p>

                    <InputError :message="form.errors.platos" />

                    <Button
                        v-if="!isGuest"
                        type="submit"
                        class="w-full bg-gradient-to-r from-emerald-600 to-emerald-800 text-white"
                        :disabled="form.processing || items.length === 0"
                    >
                        Confirmar pedido
                    </Button>
                    <Button v-else as-child class="w-full">
                        <Link :href="login().url">Iniciar sesión para pedir</Link>
                    </Button>
                </form>
            </aside>
        </div>
    </div>
</template>
