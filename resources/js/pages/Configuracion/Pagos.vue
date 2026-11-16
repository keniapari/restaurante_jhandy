<script setup lang="ts">
import { Form, Head } from '@inertiajs/vue3';
import { CreditCard, Upload } from 'lucide-vue-next';
import ConfiguracionPagoController from '@/actions/App/Http/Controllers/ConfiguracionPagoController';
import InputError from '@/components/InputError.vue';
import Heading from '@/components/Heading.vue';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';

defineProps<{
    qrPagoUrl: string | null;
}>();
</script>

<template>
    <Head title="QR de transferencia" />

    <div class="flex h-full flex-1 flex-col gap-6 rounded-xl p-4">
        <Heading
            title="QR de transferencia"
            description="Configura el código QR que verán tus clientes al hacer pedidos."
        />

        <section
            class="grid gap-6 rounded-xl border bg-card p-6 shadow-sm md:grid-cols-2"
        >
            <div class="space-y-4">
                <div class="flex items-center gap-2 text-sm font-semibold">
                    <CreditCard class="h-5 w-5 text-emerald-700" />
                    Código QR para pagos
                </div>
                <p class="text-sm text-muted-foreground">
                    Sube una imagen del QR de la cuenta bancaria del
                    restaurante. Se mostrará a los clientes en la sección de
                    pago por transferencia.
                </p>

                <Form
                    v-bind="ConfiguracionPagoController.update.form()"
                    preserve-scroll
                    class="grid gap-4"
                    v-slot="{ errors, processing }"
                >
                    <div class="grid gap-2">
                        <Label for="qr_pago">Imagen del código QR</Label>
                        <input
                            id="qr_pago"
                            type="file"
                            name="qr_pago"
                            accept=".jpg,.jpeg,.png,.webp"
                            class="block w-full rounded-md border border-input bg-background px-3 py-2 text-sm file:mr-3 file:rounded-md file:border-0 file:bg-muted file:px-3 file:py-2 file:font-medium"
                        />
                        <p class="text-xs text-muted-foreground">
                            Formatos JPG, PNG o WebP. Tamaño máximo: 4 MB.
                        </p>
                        <InputError :message="errors.qr_pago" />
                    </div>

                    <label
                        v-if="qrPagoUrl"
                        class="flex items-center gap-2 text-sm text-muted-foreground"
                    >
                        <input
                            type="checkbox"
                            name="eliminar_qr"
                            value="1"
                            class="h-4 w-4 rounded border-input accent-emerald-700"
                        />
                        Eliminar el QR actual
                    </label>
                    <InputError :message="errors.eliminar_qr" />

                    <div>
                        <Button
                            type="submit"
                            :disabled="processing"
                            class="bg-emerald-700 text-white hover:bg-emerald-800"
                        >
                            <Upload class="mr-2 h-4 w-4" />
                            Guardar cambios
                        </Button>
                    </div>
                </Form>
            </div>

            <div
                class="flex min-h-64 items-center justify-center rounded-xl border border-dashed bg-muted/30 p-5"
            >
                <img
                    v-if="qrPagoUrl"
                    :src="qrPagoUrl"
                    alt="QR de transferencia configurado"
                    class="max-h-80 max-w-full rounded-lg bg-white object-contain p-2 shadow-sm"
                />
                <p v-else class="text-center text-sm text-muted-foreground">
                    Todavía no hay un QR configurado.
                </p>
            </div>
        </section>
    </div>
</template>
