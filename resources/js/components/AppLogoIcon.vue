<script setup lang="ts">
import type { HTMLAttributes } from 'vue';

defineOptions({
    inheritAttrs: false,
});

type Props = {
    className?: HTMLAttributes['class'];
};

defineProps<Props>();
</script>

<template>
    <img
        src="/images/restaurant/logo.svg"
        alt="Logo de Restaurante Jhandy"
        :class="className"
        v-bind="$attrs"
    />
</template>
