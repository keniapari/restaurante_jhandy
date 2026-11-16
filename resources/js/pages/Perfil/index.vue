<script setup lang="ts">
import { Form, Head, Link, usePage } from '@inertiajs/vue3';
import {
    ClipboardList,
    LockKeyhole,
    Mail,
    Phone,
    ShoppingBag,
    Upload,
    UserRound,
} from 'lucide-vue-next';
import { computed } from 'vue';
import PerfilController from '@/actions/App/Http/Controllers/PerfilController';
import SecurityController from '@/actions/App/Http/Controllers/Settings/SecurityController';
import InputError from '@/components/InputError.vue';
import PasswordInput from '@/components/PasswordInput.vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { index as clienteMenuIndex } from '@/routes/cliente/menu';
import type { Cliente, Pedido } from '@/types';

const page = usePage();
const props = defineProps<{
    cliente: Cliente | null;
    pedidos: Pedido[];
    qrPagoUrl: string | null;
}>();
const user = computed(() => page.props.auth.user ?? null);

function formatCurrency(value: number): string {
    return new Intl.NumberFormat('es-BO', {
        style: 'currency',
        currency: 'BOB',
        minimumFractionDigits: 2,
    }).format(value);
}

function formatDate(iso: string): string {
    return new Date(iso).toLocaleString('es-BO', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

function resolveComprobanteUrl(ruta: string): string {
    if (/^https?:\/\//i.test(ruta) || ruta.startsWith('/')) {
        return ruta;
    }

    return `/storage/${ruta.replace(/^\/+/, '')}`;
}

function estadoBadgeClass(estado: string): string {
    switch (estado) {
        case 'Pendiente':
            return 'border-amber-300 bg-amber-50 text-amber-700';
        case 'Confirmado':
            return 'border-sky-300 bg-sky-50 text-sky-700';
        case 'En preparación':
            return 'border-orange-300 bg-orange-50 text-orange-700';
        case 'Listo':
            return 'border-emerald-300 bg-emerald-50 text-emerald-700';
        case 'Entregado':
            return 'border-emerald-400 bg-emerald-100 text-emerald-800';
        case 'Cancelado':
            return 'border-red-300 bg-red-50 text-red-700';
        default:
            return 'border-slate-300 bg-slate-50 text-slate-700';
    }
}

const defaults = computed(() => ({
    nombres: user.value?.nombres ?? '',
    apellido_paterno: user.value?.apellido_paterno ?? '',
    apellido_materno: user.value?.apellido_materno ?? '',
    telefono: user.value?.telefono ?? '',
    email: user.value?.email ?? '',
    ci_nit: props.cliente?.ci_nit ?? '',
    direccion: props.cliente?.direccion ?? '',
}));
</script>

<template>
    <Head title="Mi Perfil" />

    <div class="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-12">
        <div
            class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"
        >
            <div>
                <span
                    class="inline-flex items-center gap-1.5 rounded-full border border-amber-200/70 bg-white/70 px-4 py-1.5 text-xs font-medium text-amber-600 shadow-sm"
                >
                    <UserRound class="h-3 w-3" />
                    Área del cliente
                </span>
                <h1 class="mt-4 text-2xl font-bold text-slate-900 sm:text-3xl">
                    Mi Perfil
                </h1>
                <p class="mt-2 text-sm text-slate-500">
                    Actualiza tus datos personales y la contraseña de tu cuenta.
                </p>
            </div>
        </div>

        <div class="space-y-6">
            <section
                class="rounded-2xl border border-emerald-200/60 bg-white/80 p-6 backdrop-blur"
            >
                <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
                    <h2
                        class="flex items-center gap-2 text-lg font-bold text-slate-800"
                    >
                        <ClipboardList class="h-5 w-5 text-emerald-500" />
                        Mis pedidos
                    </h2>
                    <Button as-child class="bg-emerald-700 text-white">
                        <Link :href="clienteMenuIndex().url">
                            <ShoppingBag class="mr-2 h-4 w-4" />
                            Ver la carta
                        </Link>
                    </Button>
                </div>

                <div
                    v-if="props.pedidos.length === 0"
                    class="rounded-xl border border-dashed border-emerald-200 p-8 text-center text-sm text-muted-foreground"
                >
                    Todavía no realizaste pedidos. Explora la carta y arma tu
                    primer pedido.
                </div>

                <div v-else class="space-y-3">
                    <article
                        v-for="pedido in props.pedidos"
                        :key="pedido.id"
                        class="rounded-xl border border-emerald-100 bg-white p-4 shadow-sm"
                    >
                        <div class="flex flex-wrap items-start justify-between gap-3">
                            <div>
                                <p class="font-mono text-xs text-muted-foreground">
                                    {{ pedido.numero }}
                                </p>
                                <p class="mt-1 text-sm font-semibold text-slate-800">
                                    {{ formatDate(pedido.fecha) }}
                                </p>
                            </div>
                            <span
                                class="rounded-full border px-3 py-1 text-xs font-semibold"
                                :class="estadoBadgeClass(pedido.estado)"
                            >
                                {{ pedido.estado }}
                            </span>
                        </div>

                        <ul class="mt-3 space-y-1 text-sm text-slate-600">
                            <li
                                v-for="producto in pedido.productos"
                                :key="`${pedido.id}-${producto.nombre}`"
                                class="flex justify-between gap-4"
                            >
                                <span>
                                    {{ producto.cantidad }} ×
                                    {{ producto.nombre }}
                                </span>
                                <span class="font-medium">
                                    {{
                                        formatCurrency(
                                            producto.precio * producto.cantidad,
                                        )
                                    }}
                                </span>
                            </li>
                        </ul>

                        <div
                            class="mt-3 flex items-center justify-between border-t border-emerald-100 pt-3 text-sm"
                        >
                            <span class="capitalize text-muted-foreground">
                                Pago: {{ pedido.metodo_pago ?? '---' }}
                            </span>
                            <span class="text-base font-bold text-emerald-900">
                                {{ formatCurrency(pedido.total) }}
                            </span>
                        </div>

                        <Form
                            v-if="pedido.metodo_pago === 'transferencia'"
                            v-bind="
                                PerfilController.subirComprobante.form(
                                    pedido.id,
                                )
                            "
                            preserve-scroll
                            class="mt-4 grid gap-3 rounded-xl border border-emerald-100 bg-emerald-50/60 p-4"
                            v-slot="{ errors, processing }"
                        >
                            <div
                                class="flex flex-wrap items-center justify-between gap-2"
                            >
                                <span
                                    class="text-sm font-semibold text-emerald-950"
                                >
                                    Comprobante de transferencia
                                </span>
                                <a
                                    v-if="pedido.comprobante_pago"
                                    :href="
                                        resolveComprobanteUrl(
                                            pedido.comprobante_pago,
                                        )
                                    "
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="text-xs font-medium text-emerald-800 underline"
                                >
                                    Ver comprobante enviado
                                </a>
                            </div>
                            <img
                                v-if="props.qrPagoUrl"
                                :src="props.qrPagoUrl"
                                alt="QR para pagar el pedido por transferencia"
                                class="max-h-48 w-fit rounded-lg border border-emerald-100 bg-white object-contain p-2"
                            />
                            <input
                                type="file"
                                name="comprobante"
                                accept=".jpg,.jpeg,.png,.webp,.pdf"
                                class="block w-full text-sm text-slate-600 file:mr-3 file:rounded-md file:border-0 file:bg-emerald-100 file:px-3 file:py-2 file:font-medium file:text-emerald-800 hover:file:bg-emerald-200"
                            />
                            <InputError :message="errors.comprobante" />
                            <div>
                                <Button
                                    type="submit"
                                    size="sm"
                                    :disabled="processing"
                                    class="bg-emerald-700 text-white"
                                >
                                    <Upload class="mr-2 h-4 w-4" />
                                    {{
                                        pedido.comprobante_pago
                                            ? 'Reemplazar comprobante'
                                            : 'Agregar comprobante'
                                    }}
                                </Button>
                            </div>
                        </Form>
                    </article>
                </div>
            </section>

            <section
                class="rounded-2xl border border-emerald-200/60 bg-white/80 p-6 backdrop-blur"
            >
                <h2
                    class="mb-5 flex items-center gap-2 text-lg font-bold text-slate-800"
                >
                    <UserRound class="h-5 w-5 text-emerald-500" />
                    Datos personales
                </h2>

                <Form
                    v-bind="PerfilController.update.form()"
                    preserve-scroll
                    class="grid gap-5 sm:grid-cols-2"
                    v-slot="{ errors, processing }"
                >
                    <div class="grid gap-2">
                        <Label for="nombres">Nombres</Label>
                        <Input
                            id="nombres"
                            name="nombres"
                            type="text"
                            :default-value="defaults.nombres"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.nombres" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="apellido_paterno">Apellido paterno</Label>
                        <Input
                            id="apellido_paterno"
                            name="apellido_paterno"
                            type="text"
                            :default-value="defaults.apellido_paterno"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.apellido_paterno" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="apellido_materno">Apellido materno</Label>
                        <Input
                            id="apellido_materno"
                            name="apellido_materno"
                            type="text"
                            :default-value="defaults.apellido_materno"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.apellido_materno" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="telefono" class="flex items-center gap-1.5">
                            <Phone class="h-3.5 w-3.5 text-slate-400" />
                            Teléfono
                        </Label>
                        <Input
                            id="telefono"
                            name="telefono"
                            type="tel"
                            :default-value="defaults.telefono"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.telefono" />
                    </div>

                    <div class="grid gap-2 sm:col-span-2">
                        <Label for="email" class="flex items-center gap-1.5">
                            <Mail class="h-3.5 w-3.5 text-slate-400" />
                            Correo electrónico
                        </Label>
                        <Input
                            id="email"
                            name="email"
                            type="email"
                            :default-value="defaults.email"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.email" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="ci_nit">CI/NIT</Label>
                        <Input
                            id="ci_nit"
                            name="ci_nit"
                            type="text"
                            :default-value="defaults.ci_nit"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.ci_nit" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="direccion">Dirección</Label>
                        <Input
                            id="direccion"
                            name="direccion"
                            type="text"
                            :default-value="defaults.direccion"
                            class="border-emerald-200"
                        />
                        <InputError :message="errors.direccion" />
                    </div>

                    <div class="sm:col-span-2">
                        <Button
                            :disabled="processing"
                            class="bg-gradient-to-r from-emerald-500 to-amber-500 text-white shadow-md"
                        >
                            Guardar cambios
                        </Button>
                    </div>
                </Form>
            </section>

            <section
                class="rounded-2xl border border-emerald-200/60 bg-white/80 p-6 backdrop-blur"
            >
                <h2
                    class="mb-5 flex items-center gap-2 text-lg font-bold text-slate-800"
                >
                    <LockKeyhole class="h-5 w-5 text-emerald-500" />
                    Cambiar contraseña
                </h2>

                <Form
                    v-bind="SecurityController.update.form()"
                    preserve-scroll
                    reset-on-success
                    :reset-on-error="[
                        'current_password',
                        'password',
                        'password_confirmation',
                    ]"
                    class="grid gap-5"
                    v-slot="{ errors, processing }"
                >
                    <div class="grid gap-2">
                        <Label for="current_password">Contraseña actual</Label>
                        <PasswordInput
                            id="current_password"
                            name="current_password"
                            autocomplete="current-password"
                            placeholder="••••••••"
                        />
                        <InputError :message="errors.current_password" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="password">Nueva contraseña</Label>
                        <PasswordInput
                            id="password"
                            name="password"
                            autocomplete="new-password"
                            placeholder="••••••••"
                        />
                        <InputError :message="errors.password" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="password_confirmation"
                            >Confirmar nueva contraseña</Label
                        >
                        <PasswordInput
                            id="password_confirmation"
                            name="password_confirmation"
                            autocomplete="new-password"
                            placeholder="••••••••"
                        />
                        <InputError :message="errors.password_confirmation" />
                    </div>

                    <div>
                        <Button
                            :disabled="processing"
                            variant="outline"
                            class="border-emerald-300 text-emerald-700 hover:bg-emerald-50"
                        >
                            Actualizar contraseña
                        </Button>
                    </div>
                </Form>
            </section>
        </div>
    </div>
</template>
