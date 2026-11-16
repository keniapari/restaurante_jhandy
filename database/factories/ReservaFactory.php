<?php

namespace Database\Factories;

use App\Models\Reserva;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Reserva>
 */
class ReservaFactory extends Factory
{
    public function definition(): array
    {
        return [
            'nombre_cliente' => fake()->name(),
            'telefono' => fake()->numerify('7#######'),
            'fecha' => now()->addDays(fake()->numberBetween(1, 20))->toDateString(),
            'hora' => fake()->randomElement(['12:30', '13:00', '19:00', '20:30']),
            'personas' => fake()->numberBetween(1, 8),
            'tipo_evento' => fake()->randomElement(array_keys(Reserva::TIPOS_EVENTO)),
            'cantidad_platos' => fake()->numberBetween(11, 40),
            'metodo_pago' => fake()->randomElement(array_keys(Reserva::METODOS_PAGO)),
            'mesa' => null,
            'estado' => 'pendiente',
            'observaciones' => null,
        ];
    }
}
