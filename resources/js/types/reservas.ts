export type ReservaEstado =
    | 'pendiente'
    | 'confirmada'
    | 'completada'
    | 'cancelada';

export type ReservaMetodoPago = 'efectivo' | 'transferencia';

export type ReservaTipoEvento = 'reunion' | 'cumpleanos' | 'otra_festividad';

export type Reserva = {
    id: number;
    cliente_id: number | null;
    user_id?: number | null;
    nombre_cliente: string;
    telefono: string | null;
    fecha: string;
    hora: string;
    personas: number;
    tipo_evento: ReservaTipoEvento;
    cantidad_platos: number;
    metodo_pago: ReservaMetodoPago;
    mesa: string | null;
    estado: ReservaEstado;
    observaciones: string | null;
    created_at: string;
    updated_at: string;
    cliente?: {
        id: number;
        nombre: string;
        apellido: string | null;
        ci_nit: string | null;
    } | null;
};
