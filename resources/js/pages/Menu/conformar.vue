<script setup lang="ts">
import { Head, Link, useForm } from '@inertiajs/vue3';
import {
    ArrowLeft,
    ClipboardList,
    Minus,
    Plus,
    ShoppingBag,
    Trash2,
    UtensilsCrossed,
} from 'lucide-vue-next';
import { computed } from 'vue';
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
import { useMenuOrder } from '@/composables/useMenuOrder';
import { index as pedidosIndex } from '@/routes/gestion/pedidos';
import { conformar as menuConformar, index as menuIndex } from '@/routes/menu';
import { store as storePedido } from '@/routes/menu/conformar';
import type { Plato } from '@/types';

type ClienteOption = {
    id: number;
    nombre: string;
    apellido: string | null;
    ci_nit: string | null;
    telefono: string | null;
};

type OrderLine = {
    plato_id: number;
    cantidad: number;
};

const props = defineProps<{
    platos: Plato[];
    categorias: string[];
    clientes: ClienteOption[];
}>();

const { items, totalItems, subtotal, updateCantidad, removeItem, clearOrder } =
    useMenuOrder();

const form = useForm({
    cliente_id: '0',
    tipo: 'mesa',
    mesa: '',
    observaciones: '',
    platos: [] as OrderLine[],
});

const resumen = computed(() =>
    items.value.map((item) => ({
        ...item,
        subtotalItem: item.precio * item.cantidad,
    })),
);

function formatCurrency(value: number): string {
    return new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(value);
}

function nombreCliente(cliente: ClienteOption): string {
    const nombre = [cliente.nombre, cliente.apellido]
        .filter(Boolean)
        .join(' ');

    return cliente.ci_nit ? `${nombre} (${cliente.ci_nit})` : nombre;
}

function submit() {
    if (items.value.length === 0) {
        return;
    }

    form.platos = items.value.map((item) => ({
        plato_id: item.plato_id,
        cantidad: item.cantidad,
    }));
    form.cliente_id = form.cliente_id === '0' ? '' : form.cliente_id;

    form.post(storePedido().url, {
        preserveScroll: true,
        onSuccess: () => {
            clearOrder();
            form.reset();
        },
    });
}

defineOptions({
    layout: {
        breadcrumbs: [
            {
                title: 'Menú',
                href: menuIndex(),
            },
            {
                title: 'Conformar pedido',
                href: menuConformar(),
            },
        ],
    },
});
</script>

<template>
    <Head title="Conformar pedido" />

    <div
        class="flex h-full flex-1 flex-col gap-5 rounded-xl bg-gradient-to-br from-emerald-200 via-amber-100 to-teal-200 p-4"
    >
        <ManagementHero
            title="Conformar pedido"
            description="Revisa los platos seleccionados, define la mesa y registra el pedido."
        >
            <template #icon><ClipboardList class="h-7 w-7" /></template>
            <Button as-child variant="outline">
                <Link :href="menuIndex().url">
                    <ArrowLeft class="mr-2 h-4 w-4" />
                    Volver al menú
                </Link>
            </Button>
        </ManagementHero>

        <div
            v-if="items.length === 0"
            class="rounded-2xl border border-emerald-300 bg-white/80 p-12 text-center shadow-md"
        >
            <UtensilsCrossed class="mx-auto mb-3 h-10 w-10 text-emerald-600/50" />
            <h2 class="text-lg font-semibold text-emerald-950">
                No hay platos seleccionados
            </h2>
            <p class="mt-1 text-sm text-muted-foreground">
                Agrega platos desde el menú para conformar el pedido.
            </p>
            <Button as-child class="mt-5">
                <Link :href="menuIndex().url">Ir al menú</Link>
            </Button>
        </div>

        <div v-else class="grid gap-5 lg:grid-cols-3">
            <div class="space-y-3 lg:col-span-2">
                <div
                    class="overflow-hidden rounded-2xl border border-emerald-300 bg-white/85 shadow-xl"
                >
                    <table class="w-full text-sm">
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
                                v-for="item in resumen"
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
                                            variant="outline"
                                            size="icon-sm"
                                            @click="updateCantidad(item.plato_id, item.cantidad - 1)"
                                        >
                                            <Minus class="h-4 w-4" />
                                        </Button>
                                        <span class="w-6 text-center font-semibold">
                                            {{ item.cantidad }}
                                        </span>
                                        <Button
                                            variant="outline"
                                            size="icon-sm"
                                            @click="updateCantidad(item.plato_id, item.cantidad + 1)"
                                        >
                                            <Plus class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </td>
                                <td class="px-4 py-3 font-semibold">
                                    {{ formatCurrency(item.subtotalItem) }}
                                </td>
                                <td class="px-4 py-3 text-right">
                                    <Button
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
                                    {{ formatCurrency(subtotal) }}
                                </td>
                                <td></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <div
                    class="rounded-2xl border border-emerald-300 bg-white/80 p-4 text-sm text-muted-foreground shadow-md"
                >
                    <p>
                        {{ totalItems }}
                        {{ totalItems === 1 ? 'plato' : 'platos' }} en el pedido.
                        Al confirmar, se registrará como
                        <span class="font-semibold text-emerald-900">pendiente</span>
                        y podrás gestionarlo en
                        <Link
                            :href="pedidosIndex().url"
                            class="font-semibold text-emerald-700 underline"
                        >
                            Pedidos
                        </Link>.
                    </p>
                </div>
            </div>

            <form
                class="space-y-4 rounded-2xl border border-emerald-300 bg-white/90 p-5 shadow-xl"
                @submit.prevent="submit"
            >
                <div class="flex items-center gap-2">
                    <ShoppingBag class="h-5 w-5 text-emerald-700" />
                    <h2 class="text-base font-semibold text-emerald-950">
                        Datos del pedido
                    </h2>
                </div>

                <div class="grid gap-2">
                    <Label for="cliente_id">Cliente</Label>
                    <Select v-model="form.cliente_id">
                        <SelectTrigger class="w-full">
                            <SelectValue placeholder="Cliente mostrador" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="0">Cliente mostrador</SelectItem>
                            <SelectItem
                                v-for="cliente in props.clientes"
                                :key="cliente.id"
                                :value="String(cliente.id)"
                            >
                                {{ nombreCliente(cliente) }}
                            </SelectItem>
                        </SelectContent>
                    </Select>
                    <InputError :message="form.errors.cliente_id" />
                </div>

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

                <InputError :message="form.errors.platos" />

                <Button
                    type="submit"
                    class="w-full"
                    :disabled="form.processing || items.length === 0"
                >
                    Confirmar pedido
                </Button>
            </form>
        </div>
    </div>
</template>
