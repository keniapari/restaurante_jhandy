<?php

use App\Models\Cliente;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function usuarioAdministradorParaEstadoCliente(): User
{
    $user = User::factory()->create(['role' => Role::ADMIN]);
    $role = Role::where('nombre', Role::ADMIN)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('la administradora puede desactivar y reactivar un cliente sin eliminarlo', function () {
    $admin = usuarioAdministradorParaEstadoCliente();
    $cliente = Cliente::create([
        'nombre' => 'Cliente activo',
        'ci_nit' => 'ACT-001',
        'telefono' => '70000001',
        'estado' => 'activo',
    ]);

    $this->actingAs($admin)
        ->patch(route('clientes.estado', $cliente))
        ->assertRedirect(route('clientes.index'));

    expect($cliente->fresh()->estado)->toBe('inactivo');

    $this->actingAs($admin)
        ->patch(route('clientes.estado', $cliente))
        ->assertRedirect(route('clientes.index'));

    expect($cliente->fresh()->estado)->toBe('activo');
});

test('al conformar un pedido solo se muestran clientes activos', function () {
    $admin = usuarioAdministradorParaEstadoCliente();
    $activo = Cliente::create([
        'nombre' => 'Cliente disponible',
        'ci_nit' => 'ACT-002',
        'telefono' => '70000002',
        'estado' => 'activo',
    ]);
    $inactivo = Cliente::create([
        'nombre' => 'Cliente desactivado',
        'ci_nit' => 'INA-001',
        'telefono' => '70000003',
        'estado' => 'inactivo',
    ]);

    $this->actingAs($admin)->get(route('menu.conformar'))
        ->assertInertia(fn ($page) => $page
            ->component('Menu/conformar')
            ->where('clientes', fn ($clientes) => collect($clientes)->pluck('id')->contains($activo->id)
                && ! collect($clientes)->pluck('id')->contains($inactivo->id)));
});
