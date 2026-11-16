<script setup lang="ts">
import { Head, Link, router, useForm } from '@inertiajs/vue3';
import {
    CalendarDays,
    Pencil,
    Plus,
    Search,
    Trash2,
    Users,
} from 'lucide-vue-next';
import { computed, ref, watch } from 'vue';
import InputError from '@/components/InputError.vue';
import ManagementHero from '@/components/ManagementHero.vue';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import { usePermissions } from '@/composables/usePermissions';
import { destroy, estado, index, store, update } from '@/routes/reservas';
import type { PaginatedData, Reserva } from '@/types';

const { can } = usePermissions();

const props = defineProps<{
    reservas: PaginatedData<Reserva>;
    estados: string[];
    tiposEvento: Record<string, string>;
    metodosPago: Record<string, string>;
    filters: { search?: string };
}>();

const search = ref(props.filters.search ?? '');

function fechaLocal(offsetDias = 0): string {
    const fecha = new Date();
    fecha.setDate(fecha.getDate() + offsetDias);
    const offset = fecha.getTimezoneOffset() * 60000;

    return new Date(fecha.getTime() - offset).toISOString().slice(0, 10);
}

const fechaMinima = fechaLocal();

watch(search, (value) => {
    const url = new URL(window.location.href);

    if (value) {
        url.searchParams.set('search', value);
    } else {
        url.searchParams.delete('search');
    }

    url.searchParams.delete('page');
    setTimeout(() => {
        window.location.href = url.toString();
    }, 400);
});

function clearSearch() {
    search.value = '';
}

const createForm = useForm({
    cliente_id: '0',
    nombre_cliente: '',
    telefono: '',
    fecha: fechaLocal(1),
    hora: '',
    personas: 2,
    tipo_evento: 'reunion',
    cantidad_platos: 11,
    metodo_pago: 'efectivo',
    mesa: '',
    estado: 'pendiente',
    observaciones: '',
});

const editForm = useForm({
    cliente_id: '0',
    nombre_cliente: '',
    telefono: '',
    fecha: '',
    hora: '',
    personas: 2,
    tipo_evento: 'reunion',
    cantidad_platos: 11,
    metodo_pago: 'efectivo',
    mesa: '',
    estado: 'pendiente',
    observaciones: '',
});

const editingReserva = ref<Reserva | null>(null);
const formDialogOpen = ref(false);
const deleteDialogOpen = ref(false);
const reservaToDelete = ref<Reserva | null>(null);

const isEditing = computed(() => !!editingReserva.value);
const dialogTitle = computed(() =>
    isEditing.value ? 'Editar reserva' : 'Nueva reserva',
);
const dialogDescription = computed(() =>
    isEditing.value
        ? 'Actualiza la información de la reserva seleccionada.'
        : 'Registra una nueva reserva de mesa para el restaurante.',
);
const form = computed(() => (isEditing.value ? editForm : createForm));

function openCreateDialog() {
    editingReserva.value = null;
    createForm.reset();
    createForm.clearErrors();
    formDialogOpen.value = true;
}

function fechaParaInput(fecha: string): string {
    return fecha.slice(0, 10);
}

function openEditDialog(reserva: Reserva) {
    editingReserva.value = reserva;
    editForm.cliente_id = String(reserva.cliente_id ?? 0);
    editForm.nombre_cliente = reserva.nombre_cliente;
    editForm.telefono = reserva.telefono ?? '';
    editForm.fecha = fechaParaInput(reserva.fecha);
    editForm.hora = reserva.hora.slice(0, 5);
    editForm.personas = reserva.personas;
    editForm.tipo_evento = reserva.tipo_evento;
    editForm.cantidad_platos = reserva.cantidad_platos;
    editForm.metodo_pago = reserva.metodo_pago;
    editForm.mesa = reserva.mesa ?? '';
    editForm.estado = reserva.estado;
    editForm.observaciones = reserva.observaciones ?? '';
    editForm.clearErrors();
    formDialogOpen.value = true;
}

function submitCreate() {
    createForm.cliente_id =
        createForm.cliente_id === '0' ? '' : createForm.cliente_id;
    createForm.post(store().url, {
        preserveScroll: true,
        onSuccess: () => {
            formDialogOpen.value = false;
            createForm.reset();
        },
    });
}

function submitUpdate() {
    if (!editingReserva.value) {
        return;
    }

    editForm.cliente_id =
        editForm.cliente_id === '0' ? '' : editForm.cliente_id;
    editForm.patch(update(editingReserva.value.id).url, {
        preserveScroll: true,
        onSuccess: () => {
            formDialogOpen.value = false;
            editingReserva.value = null;
            editForm.reset();
        },
    });
}

function cambiarEstado(reserva: Reserva, nuevoEstado: string) {
    if (nuevoEstado === reserva.estado) {
        return;
    }

    router.patch(
        estado(reserva.id).url,
        { estado: nuevoEstado },
        { preserveScroll: true },
    );
}

function confirmDelete(reserva: Reserva) {
    reservaToDelete.value = reserva;
    deleteDialogOpen.value = true;
}

function submitDelete() {
    if (!reservaToDelete.value) {
        return;
    }

    const id = reservaToDelete.value.id;
    deleteDialogOpen.value = false;
    router.delete(destroy(id).url, {
        preserveScroll: true,
        onSuccess: () => {
            reservaToDelete.value = null;
        },
    });
}

function formatFecha(fecha: string): string {
    const date = new Date(`${fecha.slice(0, 10)}T00:00:00`);

    return date.toLocaleDateString('es-BO', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric',
    });
}

function estadoVariant(
    valor: string,
): 'default' | 'secondary' | 'outline' | 'destructive' {
    if (valor === 'confirmada' || valor === 'completada') {
        return 'default';
    }

    if (valor === 'cancelada') {
        return 'destructive';
    }

    return 'secondary';
}

function estadoLabel(valor: string): string {
    return valor.charAt(0).toUpperCase() + valor.slice(1);
}

function tipoEventoLabel(valor: string): string {
    return props.tiposEvento[valor] ?? valor;
}

function metodoPagoLabel(valor: string): string {
    return props.metodosPago[valor] ?? valor;
}

defineOptions({
    layout: {
        breadcrumbs: [
            {
                title: 'Registrar reservas',
                href: index(),
            },
        ],
    },
});
</script>

<template>
    <Head title="Registrar reservas" />

    <div
        class="flex h-full flex-1 flex-col gap-5 rounded-xl bg-gradient-to-br from-emerald-200 via-amber-100 to-teal-200 p-4"
    >
        <ManagementHero
            title="Registrar reservas"
            description="Gestiona las reservas de mesas y el estado de cada reserva."
        >
            <template #icon><CalendarDays class="h-7 w-7" /></template>
            <Button v-if="can('reservas.gestion')" @click="openCreateDialog">
                <Plus class="mr-2 h-4 w-4" />
                Nueva reserva
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
                    placeholder="Buscar reservas por cliente, teléfono, mesa o estado..."
                    class="pl-10"
                />
            </div>
            <Button variant="outline" @click="clearSearch">Limpiar</Button>
        </div>

        <div
            class="overflow-hidden rounded-2xl border border-emerald-300 bg-gradient-to-br from-amber-200/90 via-emerald-100/90 to-teal-200/90 shadow-xl shadow-emerald-400/25"
        >
            <table class="w-full text-sm">
                <thead>
                    <tr
                        class="border-b border-emerald-300 bg-gradient-to-r from-emerald-800 via-emerald-700 to-amber-600 text-left text-amber-50"
                    >
                        <th class="px-4 py-3 font-medium">Fecha y hora</th>
                        <th class="px-4 py-3 font-medium">Cliente</th>
                        <th class="px-4 py-3 font-medium">Personas</th>
                        <th class="px-4 py-3 font-medium">Evento</th>
                        <th class="px-4 py-3 font-medium">Mesa</th>
                        <th class="px-4 py-3 font-medium">Estado</th>
                        <th class="px-4 py-3 text-right font-medium">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="reserva in reservas.data"
                        :key="reserva.id"
                        class="border-b transition-colors last:border-0 hover:bg-muted/30"
                    >
                        <td class="px-4 py-3">
                            <div class="flex items-center gap-3">
                                <div
                                    class="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10"
                                >
                                    <CalendarDays class="h-4 w-4 text-primary" />
                                </div>
                                <div>
                                    <p class="font-medium">
                                        {{ formatFecha(reserva.fecha) }}
                                    </p>
                                    <p class="text-xs text-muted-foreground">
                                        {{ reserva.hora.slice(0, 5) }}
                                    </p>
                                </div>
                            </div>
                        </td>
                        <td class="px-4 py-3">
                            <p class="font-medium">{{ reserva.nombre_cliente }}</p>
                            <p class="text-xs text-muted-foreground">
                                {{ reserva.telefono ?? 'Sin teléfono' }}
                            </p>
                        </td>
                        <td class="px-4 py-3">
                            <Badge variant="secondary">
                                <Users class="mr-1 h-3 w-3" />
                                {{ reserva.personas }}
                            </Badge>
                        </td>
                        <td class="px-4 py-3">
                            <p class="font-medium">
                                {{ tipoEventoLabel(reserva.tipo_evento) }}
                            </p>
                            <p class="text-xs text-muted-foreground">
                                {{ reserva.cantidad_platos }} platos ·
                                {{ metodoPagoLabel(reserva.metodo_pago) }}
                            </p>
                        </td>
                        <td class="px-4 py-3">
                            <span v-if="reserva.mesa">{{ reserva.mesa }}</span>
                            <span v-else class="text-xs text-muted-foreground">—</span>
                        </td>
                        <td class="px-4 py-3">
                            <Select
                                v-if="can('reservas.gestion')"
                                :model-value="reserva.estado"
                                @update:model-value="
                                    (value) => cambiarEstado(reserva, String(value))
                                "
                            >
                                <SelectTrigger class="h-8 w-36">
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem
                                        v-for="opcion in props.estados"
                                        :key="opcion"
                                        :value="opcion"
                                    >
                                        {{ estadoLabel(opcion) }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                            <Badge v-else :variant="estadoVariant(reserva.estado)">
                                {{ estadoLabel(reserva.estado) }}
                            </Badge>
                        </td>
                        <td class="px-4 py-3 text-right">
                            <div
                                v-if="can('reservas.gestion')"
                                class="flex items-center justify-end gap-1"
                            >
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    class="border-primary/20 text-primary hover:bg-primary/10"
                                    @click="openEditDialog(reserva)"
                                >
                                    <Pencil class="h-4 w-4" />
                                </Button>
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    class="border-red-200 text-red-500 hover:bg-red-50"
                                    @click="confirmDelete(reserva)"
                                >
                                    <Trash2 class="h-4 w-4" />
                                </Button>
                            </div>
                            <span v-else class="text-xs text-muted-foreground">—</span>
                        </td>
                    </tr>
                    <tr v-if="reservas.data.length === 0">
                        <td
                            colspan="7"
                            class="py-12 text-center text-sm text-muted-foreground"
                        >
                            <CalendarDays class="mx-auto mb-2 h-8 w-8 opacity-40" />
                            No se encontraron reservas.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="reservas.last_page > 1" class="flex items-center justify-between">
            <p class="text-sm text-muted-foreground">
                Mostrando {{ reservas.from }}–{{ reservas.to }} de
                {{ reservas.total }} reservas
            </p>
            <div class="flex items-center gap-2">
                <Link
                    :href="reservas.prev_page_url ?? '#'"
                    :class="[
                        'rounded-lg border px-3 py-1.5 text-sm transition-colors',
                        reservas.prev_page_url
                            ? 'hover:bg-muted'
                            : 'pointer-events-none opacity-40',
                    ]"
                >
                    Anterior
                </Link>
                <Link
                    :href="reservas.next_page_url ?? '#'"
                    :class="[
                        'rounded-lg border px-3 py-1.5 text-sm transition-colors',
                        reservas.next_page_url
                            ? 'hover:bg-muted'
                            : 'pointer-events-none opacity-40',
                    ]"
                >
                    Siguiente
                </Link>
            </div>
        </div>
    </div>

    <Dialog v-model:open="formDialogOpen">
        <DialogContent class="sm:max-w-lg">
            <DialogHeader>
                <DialogTitle>{{ dialogTitle }}</DialogTitle>
                <DialogDescription>{{ dialogDescription }}</DialogDescription>
            </DialogHeader>
            <form @submit.prevent="isEditing ? submitUpdate() : submitCreate()">
                <div class="grid gap-4 py-4">
                    <div class="grid gap-2">
                        <Label for="nombre_cliente">Nombre del cliente *</Label>
                        <Input
                            id="nombre_cliente"
                            v-model="form.nombre_cliente"
                            placeholder="Nombre de quien reserva"
                            maxlength="160"
                        />
                        <InputError :message="form.errors.nombre_cliente" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="telefono">Teléfono</Label>
                        <Input
                            id="telefono"
                            v-model="form.telefono"
                            placeholder="Número de contacto"
                            maxlength="30"
                        />
                        <InputError :message="form.errors.telefono" />
                    </div>
                    <div class="grid gap-4 sm:grid-cols-2">
                        <div class="grid gap-2">
                            <Label for="fecha">Fecha *</Label>
                            <Input id="fecha" v-model="form.fecha" type="date" :min="fechaMinima" />
                            <InputError :message="form.errors.fecha" />
                        </div>
                        <div class="grid gap-2">
                            <Label for="hora">Hora *</Label>
                            <Input id="hora" v-model="form.hora" type="time" />
                            <InputError :message="form.errors.hora" />
                        </div>
                    </div>
                    <div
                        class="rounded-lg border border-amber-300 bg-amber-50 p-3 text-xs text-amber-800"
                    >
                        Las reservas son para una fecha futura y eventos desde 11
                        platos. El pago puede ser en efectivo o por transferencia.
                    </div>
                    <div class="grid gap-4 sm:grid-cols-2">
                        <div class="grid gap-2">
                            <Label for="personas">Personas *</Label>
                            <Input
                                id="personas"
                                v-model="form.personas"
                                type="number"
                                min="1"
                                max="50"
                            />
                            <InputError :message="form.errors.personas" />
                        </div>
                        <div class="grid gap-2">
                            <Label for="mesa">Mesa</Label>
                            <Input
                                id="mesa"
                                v-model="form.mesa"
                                placeholder="Ej: Mesa 4"
                                maxlength="20"
                            />
                            <InputError :message="form.errors.mesa" />
                        </div>
                    </div>
                    <div class="grid gap-4 sm:grid-cols-2">
                        <div class="grid gap-2">
                            <Label for="cantidad_platos">
                                Cantidad de platos *
                            </Label>
                            <Input
                                id="cantidad_platos"
                                v-model="form.cantidad_platos"
                                type="number"
                                min="11"
                                max="500"
                            />
                            <p class="text-xs text-muted-foreground">
                                Mínimo 11 platos por reserva.
                            </p>
                            <InputError
                                :message="form.errors.cantidad_platos"
                            />
                        </div>
                        <div class="grid gap-2">
                            <Label for="tipo_evento">Tipo de evento *</Label>
                            <Select v-model="form.tipo_evento">
                                <SelectTrigger class="w-full">
                                    <SelectValue
                                        placeholder="Seleccionar evento"
                                    />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem
                                        v-for="(label, valor) in props.tiposEvento"
                                        :key="valor"
                                        :value="valor"
                                    >
                                        {{ label }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                            <InputError :message="form.errors.tipo_evento" />
                        </div>
                    </div>
                    <div class="grid gap-2">
                        <Label for="metodo_pago">Método de pago *</Label>
                        <Select v-model="form.metodo_pago">
                            <SelectTrigger class="w-full">
                                <SelectValue
                                    placeholder="Seleccionar método de pago"
                                />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem
                                    v-for="(label, valor) in props.metodosPago"
                                    :key="valor"
                                    :value="valor"
                                >
                                    {{ label }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                        <InputError :message="form.errors.metodo_pago" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="estado">Estado *</Label>
                        <Select v-model="form.estado">
                            <SelectTrigger class="w-full">
                                <SelectValue placeholder="Seleccionar estado" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem
                                    v-for="opcion in props.estados"
                                    :key="opcion"
                                    :value="opcion"
                                >
                                    {{ estadoLabel(opcion) }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                        <InputError :message="form.errors.estado" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="observaciones">Observaciones</Label>
                        <textarea
                            id="observaciones"
                            v-model="form.observaciones"
                            rows="3"
                            maxlength="500"
                            placeholder="Indicaciones especiales..."
                            class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50"
                        />
                        <InputError :message="form.errors.observaciones" />
                    </div>
                </div>
                <DialogFooter>
                    <DialogClose as-child>
                        <Button type="button" variant="outline">Cancelar</Button>
                    </DialogClose>
                    <Button type="submit" :disabled="form.processing">
                        {{ isEditing ? 'Actualizar reserva' : 'Guardar reserva' }}
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>

    <Dialog v-model:open="deleteDialogOpen">
        <DialogContent class="sm:max-w-md">
            <DialogHeader>
                <DialogTitle>Eliminar reserva</DialogTitle>
                <DialogDescription>
                    ¿Está seguro de eliminar esta reserva? Esta acción no se puede
                    deshacer.
                </DialogDescription>
            </DialogHeader>
            <DialogFooter>
                <DialogClose as-child>
                    <Button type="button" variant="outline">Cancelar</Button>
                </DialogClose>
                <Button variant="destructive" @click="submitDelete">
                    Eliminar
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
