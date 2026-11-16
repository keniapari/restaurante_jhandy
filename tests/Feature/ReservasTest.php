<?php

use App\Models\Reserva;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function restauranteReservasUser(string $roleName): User
{
    $user = User::factory()->create(['role' => $roleName]);
    $role = Role::where('nombre', $roleName)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

function restauranteReservaPayload(array $overrides = []): array
{
    return array_merge([
        'nombre_cliente' => 'Ana Pérez',
        'telefono' => '70012345',
        'fecha' => now()->addDay()->toDateString(),
        'hora' => '20:30',
        'personas' => 4,
        'tipo_evento' => 'cumpleanos',
        'cantidad_platos' => 12,
        'metodo_pago' => 'transferencia',
        'mesa' => 'Mesa 3',
        'estado' => 'pendiente',
        'observaciones' => 'Cumpleaños.',
    ], $overrides);
}

test('vendedor puede listar y registrar reservas', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->get(route('reservas.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Reservas/index')
            ->has('reservas.data')
            ->has('estados'));

    $this->actingAs($vendedor)
        ->post(route('reservas.store'), restauranteReservaPayload())
        ->assertRedirect(route('reservas.index'))
        ->assertSessionHasNoErrors();

    $reserva = Reserva::sole();
    expect($reserva->nombre_cliente)->toBe('Ana Pérez')
        ->and($reserva->personas)->toBe(4)
        ->and($reserva->tipo_evento)->toBe('cumpleanos')
        ->and($reserva->cantidad_platos)->toBe(12)
        ->and($reserva->metodo_pago)->toBe('transferencia')
        ->and($reserva->user_id)->toBe($vendedor->id);
});

test('vendedor puede cambiar el estado de una reserva', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);
    $reserva = Reserva::factory()->create(['estado' => 'pendiente']);

    $this->actingAs($vendedor)
        ->patch(route('reservas.estado', $reserva), ['estado' => 'confirmada'])
        ->assertRedirect();

    expect($reserva->fresh()->estado)->toBe('confirmada');
});

test('admin puede actualizar y eliminar una reserva', function () {
    $admin = restauranteReservasUser(Role::ADMIN);
    $reserva = Reserva::factory()->create();

    $this->actingAs($admin)
        ->patch(route('reservas.update', $reserva), restauranteReservaPayload([
            'nombre_cliente' => 'Luis Gómez',
            'personas' => 6,
        ]))
        ->assertRedirect(route('reservas.index'))
        ->assertSessionHasNoErrors();

    expect($reserva->fresh()->nombre_cliente)->toBe('Luis Gómez')
        ->and($reserva->fresh()->personas)->toBe(6);

    $this->actingAs($admin)
        ->delete(route('reservas.destroy', $reserva))
        ->assertRedirect(route('reservas.index'));

    $this->assertDatabaseMissing('reservas', ['id' => $reserva->id]);
});

test('encargado de inventario no puede acceder a reservas', function () {
    $encargado = restauranteReservasUser(Role::ENCARGADO_INVENTARIO);

    $this->actingAs($encargado)->get(route('reservas.index'))->assertForbidden();
});

test('el estado de la reserva debe ser valido', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->post(route('reservas.store'), restauranteReservaPayload(['estado' => 'esperando']))
        ->assertSessionHasErrors('estado');

    $this->assertDatabaseCount('reservas', 0);
});

test('la reserva debe ser para una fecha futura', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->post(route('reservas.store'), restauranteReservaPayload([
            'fecha' => now()->subDay()->toDateString(),
        ]))
        ->assertSessionHasErrors('fecha');

    $this->assertDatabaseCount('reservas', 0);
});

test('la reserva requiere mas de 10 platos', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->post(route('reservas.store'), restauranteReservaPayload([
            'cantidad_platos' => 10,
        ]))
        ->assertSessionHasErrors('cantidad_platos');

    $this->assertDatabaseCount('reservas', 0);
});

test('la reserva valida el tipo de evento y el metodo de pago', function () {
    $vendedor = restauranteReservasUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->post(route('reservas.store'), restauranteReservaPayload([
            'tipo_evento' => 'bautizo',
            'metodo_pago' => 'cheque',
        ]))
        ->assertSessionHasErrors(['tipo_evento', 'metodo_pago']);

    $this->assertDatabaseCount('reservas', 0);
});
