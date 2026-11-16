<script setup lang="ts">
import { Form, Head } from '@inertiajs/vue3';
import { ArrowRight, LockKeyhole, Mail } from 'lucide-vue-next';
import InputError from '@/components/InputError.vue';
import PasswordInput from '@/components/PasswordInput.vue';
import TextLink from '@/components/TextLink.vue';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Spinner } from '@/components/ui/spinner';
import { redirect as googleRedirect } from '@/routes/auth/google';
import { store } from '@/routes/login';
import { request } from '@/routes/password';

defineOptions({
    layout: {
        title: 'Bienvenido de nuevo',
        description:
            'Clientes: ingresen con su cuenta de Google. Personal del restaurante: correo y contraseña.',
    },
});

defineProps<{
    status?: string;
    canResetPassword: boolean;
}>();
</script>

<template>
    <Head title="Iniciar sesión" />

    <div
        v-if="status"
        class="mb-5 rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-3 text-center text-sm font-semibold text-emerald-900"
    >
        {{ status }}
    </div>

    <InputError
        :message="$page.props.errors?.google"
        class="mb-4 text-center"
    />

    <p class="mb-3 text-xs font-semibold tracking-wide text-[#0f3d2e]/60 uppercase">
        Personal del restaurante
    </p>

    <Form
        v-bind="store()"
        :reset-on-success="['password']"
        v-slot="{ errors, processing }"
        class="flex flex-col gap-4"
    >
        <div class="grid gap-2">
            <Label
                for="email"
                class="flex items-center gap-2 text-sm font-semibold text-[#0f3d2e]"
            >
                <Mail class="size-4 text-amber-600" />
                Correo electrónico
            </Label>
            <Input
                id="email"
                type="email"
                name="email"
                required
                autofocus
                :tabindex="1"
                autocomplete="email"
                placeholder="correo@ejemplo.com"
                class="h-11 rounded-xl border-amber-200/80 bg-white text-[#0b3d2e] shadow-sm placeholder:text-[#0b3d2e]/30 focus:border-amber-500 focus:ring-amber-400/40"
            />
            <InputError :message="errors.email" />
        </div>

        <div class="grid gap-2">
            <div class="flex items-center justify-between gap-3">
                <Label
                    for="password"
                    class="flex items-center gap-2 text-sm font-semibold text-[#0f3d2e]"
                >
                    <LockKeyhole class="size-4 text-amber-600" />
                    Contraseña
                </Label>
                <TextLink
                    v-if="canResetPassword"
                    :href="request()"
                    class="text-xs font-semibold text-emerald-700 decoration-emerald-300 underline-offset-4 hover:text-amber-700"
                    :tabindex="5"
                >
                    ¿Olvidaste tu contraseña?
                </TextLink>
            </div>
            <PasswordInput
                id="password"
                name="password"
                required
                :tabindex="2"
                autocomplete="current-password"
                placeholder="••••••••"
                class="h-11 rounded-xl border-amber-200/80 bg-white text-[#0b3d2e] shadow-sm placeholder:text-[#0b3d2e]/30 focus:border-amber-500 focus:ring-amber-400/40"
            />
            <InputError :message="errors.password" />
        </div>

        <Label
            for="remember"
            class="flex w-fit items-center gap-2.5 text-sm text-[#0f3d2e]/70"
        >
            <Checkbox
                id="remember"
                name="remember"
                :tabindex="3"
                class="border-amber-400 data-[state=checked]:border-emerald-900 data-[state=checked]:bg-emerald-900"
            />
            Recordarme
        </Label>

        <Button
            type="submit"
            class="group mt-1 h-11 w-full rounded-xl bg-gradient-to-r from-[#0b3d2e] via-[#116149] to-[#0b3d2e] font-semibold text-amber-50 shadow-lg ring-1 shadow-emerald-900/30 ring-amber-400/50 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-emerald-900/40 active:translate-y-0"
            :tabindex="4"
            :disabled="processing"
            data-test="login-button"
        >
            <Spinner v-if="processing" />
            <template v-else>
                Iniciar sesión
                <ArrowRight
                    class="ml-2 size-4 transition-transform duration-200 group-hover:translate-x-0.5"
                />
            </template>
        </Button>
    </Form>

    <div class="my-5 flex items-center gap-3" aria-hidden="true">
        <span class="h-px flex-1 bg-amber-400/40"></span>
        <span class="text-xs font-medium text-[#0f3d2e]/40"
            >o continúa con</span
        >
        <span class="h-px flex-1 bg-amber-400/40"></span>
    </div>

    <a
        :href="googleRedirect().url"
        class="flex h-11 w-full items-center justify-center gap-3 rounded-xl border border-amber-200/80 bg-white px-4 text-sm font-semibold text-[#0b3d2e] shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-amber-400 hover:bg-amber-50 hover:shadow-md"
        data-test="google-login-button"
    >
        <svg class="size-5" viewBox="0 0 24 24" aria-hidden="true">
            <path
                fill="#4285F4"
                d="M21.6 12.23c0-.71-.06-1.4-.18-2.07H12v3.92h5.38a4.6 4.6 0 0 1-2 3.02v2.54h3.24c1.9-1.75 2.98-4.33 2.98-7.41Z"
            />
            <path
                fill="#34A853"
                d="M12 22c2.7 0 4.98-.9 6.64-2.36l-3.24-2.54c-.9.6-2.05.96-3.4.96-2.61 0-4.82-1.76-5.61-4.13H3.04v2.62A10 10 0 0 0 12 22Z"
            />
            <path
                fill="#FBBC05"
                d="M6.39 13.93A6.02 6.02 0 0 1 6.07 12c0-.67.12-1.32.32-1.93V7.45H3.04A10 10 0 0 0 2 12c0 1.64.39 3.19 1.04 4.55l3.35-2.62Z"
            />
            <path
                fill="#EA4335"
                d="M12 5.94c1.47 0 2.79.5 3.83 1.5l2.88-2.88A9.65 9.65 0 0 0 12 2a10 10 0 0 0-8.96 5.45l3.35 2.62C7.18 7.7 9.39 5.94 12 5.94Z"
            />
        </svg>
        Continuar con Google
    </a>

    <p class="mt-3 text-center text-xs text-[#0f3d2e]/50">
        Clientes: usen el mismo correo con el que fueron registrados en el
        restaurante.
    </p>
</template>
