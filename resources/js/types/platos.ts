export type PlatoCategoria =
    | 'Entradas'
    | 'Platos fuertes'
    | 'Postres'
    | 'Bebidas';

export type Plato = {
    id: number;
    nombre: string;
    descripcion: string | null;
    categoria: PlatoCategoria | string;
    precio: string;
    imagen: string | null;
    disponible: boolean;
    estado: string;
    created_at: string;
    updated_at: string;
};
