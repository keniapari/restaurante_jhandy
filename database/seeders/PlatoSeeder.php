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
            ['nombre' => 'Flan de caramelo', 'categoria' => 'Postres', 'precio' => 15, 'descripcion' => 'Flan casero con salsa de caramelo.'],
            ['nombre' => 'Jugo de maracuyá', 'categoria' => 'Bebidas', 'precio' => 10, 'descripcion' => 'Jugo natural de maracuyá.'],
            ['nombre' => 'Limonada', 'categoria' => 'Bebidas', 'precio' => 8, 'descripcion' => 'Limonada fresca con hierbabuena.'],
        ];

        foreach ($platos as $index => $plato) {
            Plato::updateOrCreate(
                ['nombre' => $plato['nombre']],
                [
                    ...$plato,
                    'imagen' => '/images/restaurant/plato-'.(($index % 4) + 1).'.jpg',
                    'disponible' => true,
                    'estado' => 'activo',
                ]
            );
        }
    }
}
