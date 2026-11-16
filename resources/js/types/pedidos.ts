export type PedidoEstado =
    | 'Pendiente'
    | 'Confirmado'
    | 'En preparación'
    | 'Listo'
    | 'Enviado'
    | 'Entregado'
    | 'Cancelado';

export type PedidoProducto = {
    producto_id: number | null;
    plato_id?: number | null;
    nombre: string;
    precio: number;
    cantidad: number;
    subtotal?: number;
    color: string | null;
    talla: string | null;
    imagen: string | null;
};

export type Pedido = {
    id: number;
    numero: string;
    fecha: string;
    estado: PedidoEstado;
    tipo?: 'online' | 'mesa' | 'llevar' | string;
    mesa?: string | null;
    observaciones?: string | null;
    total: number;
    metodo_pago: string | null;
    comprobante_pago?: string | null;
    productos: PedidoProducto[];
    cliente?: {
        id: number;
        nombre: string;
        email?: string;
        telefono?: string;
    } | null;
    created_at?: string;
    updated_at?: string;
};
