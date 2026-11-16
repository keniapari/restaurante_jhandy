import { computed, ref, watch } from 'vue';

export interface MenuOrderItem {
    plato_id: number;
    nombre: string;
    precio: number;
    imagen: string | null;
    cantidad: number;
}

const STORAGE_KEY = 'jhandy_menu_order_v1';

const items = ref<MenuOrderItem[]>([]);

function loadFromStorage() {
    try {
        const stored = localStorage.getItem(STORAGE_KEY);

        if (stored) {
            items.value = (JSON.parse(stored) as MenuOrderItem[]).map(
                (item) => ({
                    ...item,
                    cantidad: Math.max(1, Number(item.cantidad) || 1),
                    precio: Number(item.precio) || 0,
                }),
            );
        }
    } catch {
        items.value = [];
    }
}

function saveToStorage() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value));
}

loadFromStorage();

watch(items, saveToStorage, { deep: true });

export function useMenuOrder() {
    const totalItems = computed(() =>
        items.value.reduce((sum, item) => sum + item.cantidad, 0),
    );

    const subtotal = computed(() =>
        items.value.reduce((sum, item) => sum + item.precio * item.cantidad, 0),
    );

    function cantidadDe(platoId: number): number {
        return (
            items.value.find((item) => item.plato_id === platoId)?.cantidad ?? 0
        );
    }

    function addItem(
        plato: {
            id: number;
            nombre: string;
            precio: string | number;
            imagen: string | null;
        },
        cantidad: number = 1,
    ) {
        const existing = items.value.find(
            (item) => item.plato_id === plato.id,
        );

        if (existing) {
            existing.cantidad = Math.min(50, existing.cantidad + cantidad);
        } else {
            items.value.push({
                plato_id: plato.id,
                nombre: plato.nombre,
                precio: Number(plato.precio) || 0,
                imagen: plato.imagen,
                cantidad: Math.max(1, cantidad),
            });
        }
    }

    function updateCantidad(platoId: number, cantidad: number) {
        const item = items.value.find((i) => i.plato_id === platoId);

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
        items.value = items.value.filter((i) => i.plato_id !== platoId);
    }

    function clearOrder() {
        items.value = [];
    }

    return {
        items,
        totalItems,
        subtotal,
        cantidadDe,
        addItem,
        updateCantidad,
        removeItem,
        clearOrder,
    };
}
