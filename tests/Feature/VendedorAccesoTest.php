<?php

use App\Models\Cliente;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function usuarioConRolVendedor(): User
{
    $user = User::factory()->create(['role' => Role::VENDEDOR]);
    $role = Role::where('nombre', Role::VENDEDOR)->firstOrFail();
    $role->ensureDefaultPermissions();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

function usuarioConRolAdministrador(): User
{
    $user = User::factory()->create(['role' => Role::ADMIN]);
    $role = Role::where('nombre', Role::ADMIN)->firstOrFail();
    $role->ensureDefaultPermissions();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('el rol vendedor recibe permisos de pedidos, menu, platos y reservas', function () {
    $vendedor = usuarioConRolVendedor();

    expect($vendedor->hasPermission('pedidos.ver'))->toBeTrue()
        ->and($vendedor->hasPermission('pedidos.gestion'))->toBeFalse()
        ->and($vendedor->hasPermission('pedidos.crear'))->toBeTrue()
        ->and($vendedor->hasPermission('pedidos.confirmar'))->toBeTrue()
        ->and($vendedor->hasPermission('menu.ver'))->toBeTrue()
        ->and($vendedor->hasPermission('platos.ver'))->toBeTrue()
        ->and($vendedor->hasPermission('reservas.ver'))->toBeTrue()
        ->and($vendedor->hasPermission('reservas.gestion'))->toBeTrue()
        ->and($vendedor->hasPermission('clientes.ver'))->toBeTrue()
        ->and($vendedor->hasPermission('usuarios.gestion'))->toBeFalse();
});

test('la vendedora puede registrar un cliente y queda identificada como quien lo registro', function () {
    $vendedor = usuarioConRolVendedor();

    $this->actingAs($vendedor)->get(route('clientes.index'))->assertOk();

    $this->actingAs($vendedor)->post(route('clientes.store'), [
        'nombre' => 'Cliente atendido por vendedora',
        'apellido' => 'Perez',
        'ci_nit' => 'VEN-001',
        'telefono' => '70000111',
    ])->assertRedirect(route('clientes.index'))->assertSessionHasNoErrors();

    $cliente = Cliente::where('ci_nit', 'VEN-001')->sole();

    expect($cliente->registrado_por_user_id)->toBe($vendedor->id)
        ->and($cliente->registradoPor->is($vendedor))->toBeTrue();
});

test('la administradora ve en el listado quien registro cada cliente', function () {
    $vendedor = usuarioConRolVendedor();
    $admin = usuarioConRolAdministrador();

    $this->actingAs($vendedor)->post(route('clientes.store'), [
        'nombre' => 'Cliente visible para admin',
        'ci_nit' => 'VEN-002',
        'telefono' => '70000222',
    ])->assertSessionHasNoErrors();

    $this->actingAs($admin)->get(route('clientes.index'))
        ->assertOk()
        ->assertInertia(fn ($page) => $page
            ->where('clientes.data.0.registrado_por.id', $vendedor->id)
            ->where('clientes.data.0.registrado_por_user_id', $vendedor->id));
});

test('la vendedora accede al menu, platos y reservas pero no a usuarios', function () {
    $vendedor = usuarioConRolVendedor();

    $this->actingAs($vendedor)->get(route('menu.index'))->assertOk();
    $this->actingAs($vendedor)->get(route('menu.conformar'))->assertOk();
    $this->actingAs($vendedor)->get(route('platos.index'))->assertOk();
    $this->actingAs($vendedor)->get(route('reservas.index'))->assertOk();
    $this->actingAs($vendedor)->get(route('usuarios.index'))->assertForbidden();
});
