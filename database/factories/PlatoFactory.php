<?php

namespace Database\Factories;

use App\Models\Plato;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Plato>
 */
class PlatoFactory extends Factory
{
    public function definition(): array
    {
        return [
            'nombre' => fake()->unique()->words(3, true),
            'descripcion' => fake()->sentence(),
            'categoria' => fake()->randomElement(Plato::CATEGORIAS),
            'precio' => fake()->randomFloat(2, 15, 120),
            'imagen' => '/images/restaurant/plato-'.fake()->numberBetween(1, 4).'.jpg',
            'disponible' => true,
            'estado' => 'activo',
        ];
    }

    public function noDisponible(): static
    {
        return $this->state(fn (): array => ['disponible' => false]);
    }
}
