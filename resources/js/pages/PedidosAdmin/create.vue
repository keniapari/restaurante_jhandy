<script setup lang="ts">
import { Head, Link, useForm } from '@inertiajs/vue3';
import {
    ArrowLeft,
    Banknote,
    Landmark,
    Minus,
    Plus,
    ShoppingBag,
    Trash2,
    UserRound,
    UtensilsCrossed,
} from 'lucide-vue-next';
import { computed, ref } from 'vue';
import InputError from '@/components/InputError.vue';
import ManagementHero from '@/components/ManagementHero.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import {
    create as pedidosCreate,
    index as pedidosIndex,
    store as storePedido,
} from '@/routes/gestion/pedidos';
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
}>();

const items = ref<OrderLine[]>([]);
const categoriaActiva = ref('Todas');
const busqueda = ref('');

const form = useForm({
    cliente_nombre: '',
    cliente_apellido: '',
    cliente_ci_nit: '',
    cliente_telefono: '',
    tipo: 'mesa',
    mesa: '',
    metodo_pago: 'efectivo',
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
            termino === '' || plato.nombre.toLowerCase().includes(termino);

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
        onSuccess: () => {
            items.value = [];
            form.reset();
        },
    });
}

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Pedidos', href: pedidosIndex() },
            { title: 'Nuevo pedido', href: pedidosCreate() },
        ],
    },
});
</script>

<template>
    <Head title="Nuevo pedido" />

    <div
        class="flex h-full flex-1 flex-col gap-5 rounded-xl bg-gradient-to-br from-emerald-200 via-amber-100 to-teal-200 p-4"
    >
        <ManagementHero
            title="Nuevo pedido"
            description="Registra los datos del cliente, selecciona los platos del menú y define el pago."
        >
            <template #icon><ShoppingBag class="h-7 w-7" /></template>
            <Button as-child variant="outline">
                <Link :href="pedidosIndex().url">
                    <ArrowLeft class="mr-2 h-4 w-4" />
                    Volver a pedidos
                </Link>
            </Button>
        </ManagementHero>

        <form class="grid gap-5 xl:grid-cols-3" @submit.prevent="submit">
            <div class="space-y-5 xl:col-span-2">
                <section
                    class="rounded-2xl border border-emerald-300 bg-white/85 p-5 shadow-xl"
                >
                    <div class="mb-4 flex items-center gap-2">
                        <UserRound class="h-5 w-5 text-emerald-700" />
                        <h2 class="text-base font-semibold text-emerald-950">
                            Datos del cliente
                        </h2>
                    </div>

                    <div class="grid gap-4 sm:grid-cols-2">
                        <div class="grid gap-2">
                            <Label for="cliente_nombre">Nombre *</Label>
                            <Input
                                id="cliente_nombre"
                                v-model="form.cliente_nombre"
                                placeholder="Ej: María"
                                maxlength="160"
                            />
                            <InputError :message="form.errors.cliente_nombre" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="cliente_apellido">Apellido</Label>
                            <Input
                                id="cliente_apellido"
                                v-model="form.cliente_apellido"
                                placeholder="Ej: Quispe"
                                maxlength="160"
                            />
                            <InputError :message="form.errors.cliente_apellido" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="cliente_ci_nit">CI / NIT *</Label>
                            <Input
                                id="cliente_ci_nit"
                                v-model="form.cliente_ci_nit"
                                placeholder="Ej: 7894561"
                                maxlength="20"
                            />
                            <InputError :message="form.errors.cliente_ci_nit" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="cliente_telefono">Teléfono *</Label>
                            <Input
                                id="cliente_telefono"
                                v-model="form.cliente_telefono"
                                placeholder="Ej: 70012345"
                                maxlength="30"
                            />
                            <InputError :message="form.errors.cliente_telefono" />
                        </div>
                    </div>
                </section>

                <section
                    class="rounded-2xl border border-emerald-300 bg-white/85 p-5 shadow-xl"
                >
                    <div class="mb-4 flex items-center gap-2">
                        <UtensilsCrossed class="h-5 w-5 text-emerald-700" />
                        <h2 class="text-base font-semibold text-emerald-950">
                            Selecciona los platos
                        </h2>
                    </div>

                    <div class="mb-4 flex flex-wrap items-center gap-2">
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
                        <Input
                            v-model="busqueda"
                            placeholder="Buscar plato..."
                            class="ml-auto h-9 w-full sm:w-56"
                        />
                    </div>

                    <div
                        v-if="platosFiltrados.length === 0"
                        class="rounded-xl border border-dashed border-emerald-300 p-8 text-center text-sm text-muted-foreground"
                    >
                        No se encontraron platos disponibles.
                    </div>

                    <div v-else class="grid gap-3 sm:grid-cols-2">
                        <article
                            v-for="plato in platosFiltrados"
                            :key="plato.id"
                            class="flex items-center gap-3 rounded-xl border border-emerald-200 bg-white p-3 shadow-sm"
                        >
                            <img
                                :src="plato.imagen ?? '/images/restaurant/plato-1.jpg'"
                                :alt="plato.nombre"
                                class="h-14 w-14 rounded-lg object-cover"
                            />
                            <div class="min-w-0 flex-1">
                                <p class="truncate font-semibold text-emerald-950">
                                    {{ plato.nombre }}
                                </p>
                                <p class="text-xs text-muted-foreground">
                                    {{ plato.categoria }}
                                </p>
                                <p class="text-sm font-bold text-emerald-800">
                                    {{ formatCurrency(Number(plato.precio)) }}
                                </p>
                            </div>
                            <div class="flex items-center gap-1">
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
                                    Agregar
                                </Button>
                            </div>
                        </article>
                    </div>
                </section>

                <section
                    class="overflow-hidden rounded-2xl border border-emerald-300 bg-white/90 shadow-xl"
                >
                    <div class="flex items-center gap-2 border-b border-emerald-200 p-4">
                        <ShoppingBag class="h-5 w-5 text-emerald-700" />
                        <h2 class="text-base font-semibold text-emerald-950">
                            Pedido seleccionado
                        </h2>
                    </div>

                    <div
                        v-if="items.length === 0"
                        class="p-8 text-center text-sm text-muted-foreground"
                    >
                        Aún no agregaste platos al pedido.
                    </div>

                    <table v-else class="w-full text-sm">
                        <thead>
                            <tr
                                class="border-b border-emerald-300 bg-gradient-to-r from-emerald-800 via-emerald-700 to-amber-600 text-left text-amber-50"
                            >
                                <th class="px-4 py-3 font-medium">Plato</th>
                                <th class="px-4 py-3 font-medium">Precio</th>
                                <th class="px-4 py-3 font-medium">Cantidad</th>
                                <th class="px-4 py-3 font-medium">Subtotal</th>
                                <th class="px-4 py-3 text-right font-medium"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="item in items"
                                :key="item.plato_id"
                                class="border-b last:border-0"
                            >
                                <td class="px-4 py-3">
                                    <div class="flex items-center gap-3">
                                        <img
                                            :src="item.imagen ?? '/images/restaurant/plato-1.jpg'"
                                            :alt="item.nombre"
                                            class="h-10 w-10 rounded-lg object-cover"
                                        />
                                        <span class="font-medium">{{ item.nombre }}</span>
                                    </div>
                                </td>
                                <td class="px-4 py-3">
                                    {{ formatCurrency(item.precio) }}
                                </td>
                                <td class="px-4 py-3">
                                    <div class="flex items-center gap-2">
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
                                            <Minus class="h-4 w-4" />
                                        </Button>
                                        <span class="w-6 text-center font-semibold">
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
                                            <Plus class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </td>
                                <td class="px-4 py-3 font-semibold">
                                    {{ formatCurrency(item.precio * item.cantidad) }}
                                </td>
                                <td class="px-4 py-3 text-right">
                                    <Button
                                        type="button"
                                        variant="outline"
                                        size="icon-sm"
                                        class="border-red-200 text-red-500 hover:bg-red-50"
                                        @click="removeItem(item.plato_id)"
                                    >
                                        <Trash2 class="h-4 w-4" />
                                    </Button>
                                </td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr class="border-t border-emerald-300 bg-emerald-50/80">
                                <td colspan="3" class="px-4 py-3 text-right font-medium">
                                    Total del pedido
                                </td>
                                <td class="px-4 py-3 text-lg font-bold text-emerald-900">
                                    {{ formatCurrency(total) }}
                                </td>
                                <td></td>
                            </tr>
                        </tfoot>
                    </table>
                </section>
            </div>

            <aside class="space-y-4">
                <div
                    class="space-y-4 rounded-2xl border border-emerald-300 bg-white/90 p-5 shadow-xl"
                >
                    <h2 class="text-base font-semibold text-emerald-950">
                        Detalles del pedido
                    </h2>

                    <div class="grid gap-2">
                        <Label for="tipo">Tipo de pedido *</Label>
                        <Select v-model="form.tipo">
                            <SelectTrigger class="w-full">
                                <SelectValue placeholder="Seleccionar tipo" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="mesa">Consumo en mesa</SelectItem>
                                <SelectItem value="llevar">Para llevar</SelectItem>
                            </SelectContent>
                        </Select>
                        <InputError :message="form.errors.tipo" />
                    </div>

                    <div v-if="form.tipo === 'mesa'" class="grid gap-2">
                        <Label for="mesa">Mesa *</Label>
                        <Input
                            id="mesa"
                            v-model="form.mesa"
                            placeholder="Ej: Mesa 4"
                            maxlength="20"
                        />
                        <InputError :message="form.errors.mesa" />
                    </div>

                    <div class="grid gap-2">
                        <Label>Forma de pago *</Label>
                        <div class="grid grid-cols-2 gap-2">
                            <button
                                type="button"
                                class="flex items-center justify-center gap-2 rounded-xl border px-3 py-2.5 text-sm font-semibold transition"
                                :class="
                                    form.metodo_pago === 'efectivo'
                                        ? 'border-emerald-700 bg-emerald-700 text-white shadow'
                                        : 'border-emerald-200 bg-white text-emerald-800 hover:border-emerald-500'
                                "
                                @click="form.metodo_pago = 'efectivo'"
                            >
                                <Banknote class="h-4 w-4" />
                                Efectivo
                            </button>
                            <button
                                type="button"
                                class="flex items-center justify-center gap-2 rounded-xl border px-3 py-2.5 text-sm font-semibold transition"
                                :class="
                                    form.metodo_pago === 'transferencia'
                                        ? 'border-emerald-700 bg-emerald-700 text-white shadow'
                                        : 'border-emerald-200 bg-white text-emerald-800 hover:border-emerald-500'
                                "
                                @click="form.metodo_pago = 'transferencia'"
                            >
                                <Landmark class="h-4 w-4" />
                                Transferencia
                            </button>
                        </div>
                        <InputError :message="form.errors.metodo_pago" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="observaciones">Observaciones</Label>
                        <textarea
                            id="observaciones"
                            v-model="form.observaciones"
                            rows="3"
                            maxlength="500"
                            placeholder="Indicaciones especiales del cliente..."
                            class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50"
                        />
                        <InputError :message="form.errors.observaciones" />
                    </div>
                </div>

                <div
                    class="rounded-2xl border border-emerald-300 bg-white/90 p-5 shadow-xl"
                >
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-muted-foreground">Platos</span>
                        <span class="font-semibold">{{ totalItems }}</span>
                    </div>
                    <div class="mt-2 flex items-center justify-between">
                        <span class="font-semibold text-emerald-950">Total</span>
                        <span class="text-2xl font-bold text-emerald-900">
                            {{ formatCurrency(total) }}
                        </span>
                    </div>

                    <InputError :message="form.errors.platos" class="mt-3" />

                    <Button
                        type="submit"
                        class="mt-4 w-full"
                        :disabled="form.processing || items.length === 0"
                    >
                        Registrar pedido
                    </Button>
                </div>
            </aside>
        </form>
    </div>
</template>
