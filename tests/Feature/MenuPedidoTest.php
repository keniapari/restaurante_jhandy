<?php

use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function restauranteMenuUser(string $roleName): User
{
    $user = User::factory()->create(['role' => $roleName]);
    $role = Role::where('nombre', $roleName)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('el menu solo muestra platos activos y disponibles', function () {
    $vendedor = restauranteMenuUser(Role::VENDEDOR);

    $disponible = Plato::factory()->create(['nombre' => 'Silpancho', 'precio' => 35]);
    Plato::factory()->noDisponible()->create(['nombre' => 'Plato agotado']);
    Plato::factory()->create(['nombre' => 'Plato inactivo', 'estado' => 'inactivo']);

    $this->actingAs($vendedor)
        ->get(route('menu.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Menu/index')
            ->has('platos', 1)
            ->where('platos.0.id', $disponible->id));
});

test('vendedor puede conformar un pedido de restaurante', function () {
    $vendedor = restauranteMenuUser(Role::VENDEDOR);
    $cliente = Cliente::factory()->create();
    $plato = Plato::factory()->create(['nombre' => 'Pique macho', 'precio' => 55]);

    $response = $this->actingAs($vendedor)->post(route('menu.conformar.store'), [
        'cliente_id' => $cliente->id,
        'tipo' => 'mesa',
        'mesa' => 'Mesa 2',
        'observaciones' => 'Sin locoto',
        'platos' => [
            ['plato_id' => $plato->id, 'cantidad' => 2],
        ],
    ]);

    $pedido = Pedido::with('detalles')->sole();

    $response->assertRedirect(route('gestion.pedidos.show', $pedido));

    expect($pedido->cliente_id)->toBe($cliente->id)
        ->and($pedido->tipo)->toBe('mesa')
        ->and($pedido->mesa)->toBe('Mesa 2')
        ->and($pedido->observaciones)->toBe('Sin locoto')
        ->and((float) $pedido->total)->toBe(110.0)
        ->and($pedido->detalles)->toHaveCount(1)
        ->and($pedido->detalles->first()->plato_id)->toBe($plato->id)
        ->and($pedido->detalles->first()->producto)->toBe('Pique macho')
        ->and($pedido->detalles->first()->cantidad)->toBe(2);
});

test('un pedido para llevar no requiere mesa', function () {
    $vendedor = restauranteMenuUser(Role::VENDEDOR);
    $plato = Plato::factory()->create(['precio' => 10]);

    $this->actingAs($vendedor)
        ->post(route('menu.conformar.store'), [
            'tipo' => 'llevar',
            'platos' => [['plato_id' => $plato->id, 'cantidad' => 1]],
        ])
        ->assertSessionHasNoErrors();

    expect(Pedido::sole()->tipo)->toBe('llevar')
        ->and(Pedido::sole()->mesa)->toBeNull();
});

test('un pedido en mesa requiere numero de mesa', function () {
    $vendedor = restauranteMenuUser(Role::VENDEDOR);
    $plato = Plato::factory()->create();

    $this->actingAs($vendedor)
        ->post(route('menu.conformar.store'), [
            'tipo' => 'mesa',
            'platos' => [['plato_id' => $plato->id, 'cantidad' => 1]],
        ])
        ->assertSessionHasErrors('mesa');

    $this->assertDatabaseCount('pedidos', 0);
});

test('no se puede conformar un pedido con un plato no disponible', function () {
    $vendedor = restauranteMenuUser(Role::VENDEDOR);
    $plato = Plato::factory()->noDisponible()->create();

    $this->actingAs($vendedor)
        ->post(route('menu.conformar.store'), [
            'tipo' => 'llevar',
            'platos' => [['plato_id' => $plato->id, 'cantidad' => 1]],
        ])
        ->assertSessionHasErrors('platos');

    $this->assertDatabaseCount('pedidos', 0);
});
