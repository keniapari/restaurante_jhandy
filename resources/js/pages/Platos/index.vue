<script setup lang="ts">
import { Head, Link, router, useForm } from '@inertiajs/vue3';
import {
    ChefHat,
    CircleCheck,
    CircleX,
    Pencil,
    Plus,
    Search,
    Trash2,
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
import { destroy, index, store, update } from '@/routes/platos';
import { update as updateDisponibilidad } from '@/routes/platos/disponibilidad';
import type { PaginatedData, Plato } from '@/types';

const { can } = usePermissions();

const props = defineProps<{
    platos: PaginatedData<Plato>;
    categorias: string[];
    filters: { search?: string };
}>();

const search = ref(props.filters.search ?? '');

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
    nombre: '',
    descripcion: '',
    categoria: 'Platos fuertes',
    precio: '',
    imagen: '',
    disponible: true,
    estado: 'activo',
});

const editForm = useForm({
    nombre: '',
    descripcion: '',
    categoria: 'Platos fuertes',
    precio: '',
    imagen: '',
    disponible: true,
    estado: 'activo',
});

const editingPlato = ref<Plato | null>(null);
const formDialogOpen = ref(false);
const deleteDialogOpen = ref(false);
const platoToDelete = ref<Plato | null>(null);

const isEditing = computed(() => !!editingPlato.value);
const dialogTitle = computed(() =>
    isEditing.value ? 'Editar plato' : 'Nuevo plato',
);
const dialogDescription = computed(() =>
    isEditing.value
        ? 'Actualiza la información del plato seleccionado.'
        : 'Registra un nuevo plato en el menú del restaurante.',
);
const form = computed(() => (isEditing.value ? editForm : createForm));

function openCreateDialog() {
    editingPlato.value = null;
    createForm.reset();
    createForm.clearErrors();
    formDialogOpen.value = true;
}

function openEditDialog(plato: Plato) {
    editingPlato.value = plato;
    editForm.nombre = plato.nombre;
    editForm.descripcion = plato.descripcion ?? '';
    editForm.categoria = plato.categoria;
    editForm.precio = String(plato.precio);
    editForm.imagen = plato.imagen ?? '';
    editForm.disponible = plato.disponible;
    editForm.estado = plato.estado;
    editForm.clearErrors();
    formDialogOpen.value = true;
}

function submitCreate() {
    createForm.post(store().url, {
        preserveScroll: true,
        onSuccess: () => {
            formDialogOpen.value = false;
            createForm.reset();
        },
    });
}

function submitUpdate() {
    if (!editingPlato.value) {
        return;
    }

    editForm.patch(update(editingPlato.value.id).url, {
        preserveScroll: true,
        onSuccess: () => {
            formDialogOpen.value = false;
            editingPlato.value = null;
            editForm.reset();
        },
    });
}

function toggleDisponibilidad(plato: Plato) {
    router.patch(
        updateDisponibilidad(plato.id).url,
        { disponible: !plato.disponible },
        { preserveScroll: true },
    );
}

function confirmDelete(plato: Plato) {
    platoToDelete.value = plato;
    deleteDialogOpen.value = true;
}

function submitDelete() {
    if (!platoToDelete.value) {
        return;
    }

    const id = platoToDelete.value.id;
    deleteDialogOpen.value = false;
    router.delete(destroy(id).url, {
        preserveScroll: true,
        onSuccess: () => {
            platoToDelete.value = null;
        },
    });
}

function formatCurrency(value: string | number): string {
    return new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(Number(value));
}

defineOptions({
    layout: {
        breadcrumbs: [
            {
                title: 'Registrar platos',
                href: index(),
            },
        ],
    },
});
</script>

<template>
    <Head title="Registrar platos" />

    <div
        class="flex h-full flex-1 flex-col gap-5 rounded-xl bg-gradient-to-br from-emerald-200 via-amber-100 to-teal-200 p-4"
    >
        <ManagementHero
            title="Registrar platos"
            description="Administra el menú del restaurante y la disponibilidad de cada plato."
        >
            <template #icon><ChefHat class="h-7 w-7" /></template>
            <Button v-if="can('platos.gestion')" @click="openCreateDialog">
                <Plus class="mr-2 h-4 w-4" />
                Nuevo plato
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
                    placeholder="Buscar platos por nombre, categoría o descripción..."
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
                        <th class="px-4 py-3 font-medium">Plato</th>
                        <th class="px-4 py-3 font-medium">Categoría</th>
                        <th class="px-4 py-3 font-medium">Precio</th>
                        <th class="px-4 py-3 font-medium">Disponibilidad</th>
                        <th class="px-4 py-3 font-medium">Estado</th>
                        <th class="px-4 py-3 text-right font-medium">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="plato in platos.data"
                        :key="plato.id"
                        class="border-b transition-colors last:border-0 hover:bg-muted/30"
                    >
                        <td class="px-4 py-3">
                            <div class="flex items-center gap-3">
                                <img
                                    :src="plato.imagen ?? '/images/restaurant/plato-1.jpg'"
                                    :alt="plato.nombre"
                                    class="h-10 w-10 rounded-lg object-cover"
                                />
                                <div>
                                    <p class="font-medium">{{ plato.nombre }}</p>
                                    <p class="line-clamp-1 text-xs text-muted-foreground">
                                        {{ plato.descripcion ?? 'Sin descripción' }}
                                    </p>
                                </div>
                            </div>
                        </td>
                        <td class="px-4 py-3">
                            <Badge variant="secondary">{{ plato.categoria }}</Badge>
                        </td>
                        <td class="px-4 py-3 font-semibold">
                            {{ formatCurrency(plato.precio) }}
                        </td>
                        <td class="px-4 py-3">
                            <Button
                                v-if="can('platos.gestion')"
                                variant="outline"
                                size="sm"
                                :class="
                                    plato.disponible
                                        ? 'border-emerald-300 text-emerald-700 hover:bg-emerald-50'
                                        : 'border-red-200 text-red-600 hover:bg-red-50'
                                "
                                @click="toggleDisponibilidad(plato)"
                            >
                                <CircleCheck
                                    v-if="plato.disponible"
                                    class="mr-1 h-4 w-4"
                                />
                                <CircleX v-else class="mr-1 h-4 w-4" />
                                {{ plato.disponible ? 'Disponible' : 'No disponible' }}
                            </Button>
                            <Badge v-else :variant="plato.disponible ? 'default' : 'secondary'">
                                {{ plato.disponible ? 'Disponible' : 'No disponible' }}
                            </Badge>
                        </td>
                        <td class="px-4 py-3">
                            <Badge :variant="plato.estado === 'activo' ? 'default' : 'outline'">
                                {{ plato.estado === 'activo' ? 'Activo' : 'Inactivo' }}
                            </Badge>
                        </td>
                        <td class="px-4 py-3 text-right">
                            <div
                                v-if="can('platos.gestion')"
                                class="flex items-center justify-end gap-1"
                            >
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    class="border-primary/20 text-primary hover:bg-primary/10"
                                    @click="openEditDialog(plato)"
                                >
                                    <Pencil class="h-4 w-4" />
                                </Button>
                                <Button
                                    variant="outline"
                                    size="icon-sm"
                                    class="border-red-200 text-red-500 hover:bg-red-50"
                                    @click="confirmDelete(plato)"
                                >
                                    <Trash2 class="h-4 w-4" />
                                </Button>
                            </div>
                            <span v-else class="text-xs text-muted-foreground">—</span>
                        </td>
                    </tr>
                    <tr v-if="platos.data.length === 0">
                        <td
                            colspan="6"
                            class="py-12 text-center text-sm text-muted-foreground"
                        >
                            <ChefHat class="mx-auto mb-2 h-8 w-8 opacity-40" />
                            No se encontraron platos.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="platos.last_page > 1" class="flex items-center justify-between">
            <p class="text-sm text-muted-foreground">
                Mostrando {{ platos.from }}–{{ platos.to }} de
                {{ platos.total }} platos
            </p>
            <div class="flex items-center gap-2">
                <Link
                    :href="platos.prev_page_url ?? '#'"
                    :class="[
                        'rounded-lg border px-3 py-1.5 text-sm transition-colors',
                        platos.prev_page_url
                            ? 'hover:bg-muted'
                            : 'pointer-events-none opacity-40',
                    ]"
                >
                    Anterior
                </Link>
                <Link
                    :href="platos.next_page_url ?? '#'"
                    :class="[
                        'rounded-lg border px-3 py-1.5 text-sm transition-colors',
                        platos.next_page_url
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
                        <Label for="nombre">Nombre del plato *</Label>
                        <Input
                            id="nombre"
                            v-model="form.nombre"
                            placeholder="Ej: Silpancho"
                            maxlength="120"
                        />
                        <InputError :message="form.errors.nombre" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="categoria">Categoría *</Label>
                        <Select v-model="form.categoria">
                            <SelectTrigger class="w-full">
                                <SelectValue placeholder="Seleccionar categoría" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem
                                    v-for="categoria in props.categorias"
                                    :key="categoria"
                                    :value="categoria"
                                >
                                    {{ categoria }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                        <InputError :message="form.errors.categoria" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="precio">Precio (Bs.) *</Label>
                        <Input
                            id="precio"
                            v-model="form.precio"
                            type="number"
                            min="0"
                            step="0.01"
                            placeholder="0.00"
                        />
                        <InputError :message="form.errors.precio" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="descripcion">Descripción</Label>
                        <textarea
                            id="descripcion"
                            v-model="form.descripcion"
                            rows="3"
                            maxlength="500"
                            placeholder="Ingredientes o detalles del plato..."
                            class="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50"
                        />
                        <InputError :message="form.errors.descripcion" />
                    </div>
                    <div class="grid gap-2">
                        <Label for="imagen">Imagen (URL)</Label>
                        <Input
                            id="imagen"
                            v-model="form.imagen"
                            placeholder="/images/restaurant/plato-1.jpg"
                            maxlength="500"
                        />
                        <InputError :message="form.errors.imagen" />
                    </div>
                    <div class="flex items-center gap-3">
                        <input
                            id="disponible"
                            v-model="form.disponible"
                            type="checkbox"
                            class="h-4 w-4 rounded border-emerald-400 text-emerald-700"
                        />
                        <Label for="disponible">Disponible para pedidos</Label>
                    </div>
                    <div class="grid gap-2">
                        <Label for="estado">Estado *</Label>
                        <Select v-model="form.estado">
                            <SelectTrigger class="w-full">
                                <SelectValue placeholder="Seleccionar estado" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="activo">Activo</SelectItem>
                                <SelectItem value="inactivo">Inactivo</SelectItem>
                            </SelectContent>
                        </Select>
                        <InputError :message="form.errors.estado" />
                    </div>
                </div>
                <DialogFooter>
                    <DialogClose as-child>
                        <Button type="button" variant="outline">Cancelar</Button>
                    </DialogClose>
                    <Button type="submit" :disabled="form.processing">
                        {{ isEditing ? 'Actualizar plato' : 'Guardar plato' }}
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>

    <Dialog v-model:open="deleteDialogOpen">
        <DialogContent class="sm:max-w-md">
            <DialogHeader>
                <DialogTitle>Eliminar plato</DialogTitle>
                <DialogDescription>
                    ¿Está seguro de eliminar este plato del menú? Los pedidos ya
                    registrados conservarán su detalle.
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
