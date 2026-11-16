<?php

use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function clienteMenuUser(): User
{
    $user = User::factory()->create(['role' => Role::CLIENTE]);
    $role = Role::where('nombre', Role::CLIENTE)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('el cliente ve la carta con los platos disponibles', function () {
    $cliente = clienteMenuUser();
    $plato = Plato::factory()->create(['nombre' => 'Silpancho', 'precio' => 35]);

    Plato::factory()->noDisponible()->create(['nombre' => 'Plato agotado']);

    $this->actingAs($cliente)
        ->get(route('cliente.menu.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Cliente/Menu')
            ->has('platos', 1)
            ->where('platos.0.id', $plato->id));
});

test('el cliente confirma un pedido para llevar con pago por transferencia', function () {
    $cliente = clienteMenuUser();
    $plato = Plato::factory()->create(['nombre' => 'Pique macho', 'precio' => 55]);

    $this->actingAs($cliente)
        ->post(route('cliente.menu.store'), [
            'observaciones' => 'Sin locoto',
            'platos' => [
                ['plato_id' => $plato->id, 'cantidad' => 2],
            ],
        ])
        ->assertRedirect(route('perfil'))
        ->assertSessionHasNoErrors();

    $pedido = Pedido::with('detalles')->sole();

    expect($pedido->cliente_id)->toBe($cliente->cliente->id)
        ->and($pedido->tipo)->toBe('llevar')
        ->and($pedido->metodo_pago)->toBe('transferencia')
        ->and($pedido->estado)->toBe(Pedido::ESTADO_PENDIENTE)
        ->and((float) $pedido->total)->toBe(110.0)
        ->and($pedido->detalles)->toHaveCount(1)
        ->and($pedido->detalles->first()->producto)->toBe('Pique macho');
});
