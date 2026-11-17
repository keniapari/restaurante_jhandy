<?php

namespace Database\Seeders;

use App\Models\Plato;
use Illuminate\Database\Seeder;

class PlatoSeeder extends Seeder
{
    public function run(): void
    {
        $platos = [
            ['nombre' => 'Sopa de maní', 'categoria' => 'Entradas', 'precio' => 18, 'descripcion' => 'Sopa tradicional con maní tostado, papas y fideo.'],
            ['nombre' => 'Ensalada de la casa', 'categoria' => 'Entradas', 'precio' => 22, 'descripcion' => 'Lechuga, tomate, zanahoria y aderezo de la casa.'],
            ['nombre' => 'Silpancho', 'categoria' => 'Platos fuertes', 'precio' => 35, 'descripcion' => 'Carne apanada, arroz, papa y huevo.'],
            ['nombre' => 'Pique macho', 'categoria' => 'Platos fuertes', 'precio' => 55, 'descripcion' => 'Carne de res, papas fritas, salchicha y locoto.'],
            ['nombre' => 'Pollo a la plancha', 'categoria' => 'Platos fuertes', 'precio' => 38, 'descripcion' => 'Pechuga de pollo con guarnición de arroz y ensalada.'],
            ['nombre' => 'Gaseosa', 'categoria' => 'Bebidas', 'precio' => 8, 'descripcion' => 'Gaseosa fría de varios sabores.'],
            ['nombre' => 'Hervido', 'categoria' => 'Bebidas', 'precio' => 10, 'descripcion' => 'Bebida caliente tradicional.'],
            ['nombre' => 'Cerveza', 'categoria' => 'Bebidas', 'precio' => 15, 'descripcion' => 'Cerveza fría.'],
        ];

        foreach ($platos as $index => $plato) {
            $imagenesComida = [
                '/images/restaurant/plato-1.jpg',
                '/images/restaurant/plato-3.jpg',
                '/images/restaurant/plato-4.jpg',
            ];
            Plato::updateOrCreate(
                ['nombre' => $plato['nombre']],
                [
                    ...$plato,
                    'imagen' => $imagenesComida[$index % count($imagenesComida)],
                    'disponible' => true,
                    'estado' => 'activo',
                ]
            );
        }
    }
}
