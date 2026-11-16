<?php

use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function nuevoPedidoUser(string $roleName): User
{
    $user = User::factory()->create(['role' => $roleName]);
    $role = Role::where('nombre', $roleName)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('el formulario de nuevo pedido muestra los platos disponibles', function () {
    $vendedor = nuevoPedidoUser(Role::VENDEDOR);

    $plato = Plato::factory()->create(['nombre' => 'Silpancho']);
    Plato::factory()->noDisponible()->create();

    $this->actingAs($vendedor)
        ->get(route('gestion.pedidos.create'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('PedidosAdmin/create')
            ->has('platos', 1)
            ->where('platos.0.id', $plato->id)
            ->has('categorias'));
});

test('vendedor registra un pedido con cliente nuevo, platos y pago en efectivo', function () {
    $vendedor = nuevoPedidoUser(Role::VENDEDOR);
    $plato = Plato::factory()->create(['nombre' => 'Pique macho', 'precio' => 55]);
    $bebida = Plato::factory()->create(['nombre' => 'Jugo', 'precio' => 10]);

    $this->actingAs($vendedor)
        ->post(route('gestion.pedidos.store'), [
            'cliente_nombre' => 'María',
            'cliente_apellido' => 'Quispe',
            'cliente_ci_nit' => '7894561',
            'cliente_telefono' => '70012345',
            'tipo' => 'mesa',
            'mesa' => 'Mesa 4',
            'metodo_pago' => 'efectivo',
            'observaciones' => 'Sin locoto',
            'platos' => [
                ['plato_id' => $plato->id, 'cantidad' => 2],
                ['plato_id' => $bebida->id, 'cantidad' => 1],
            ],
        ])
        ->assertSessionHasNoErrors();

    $cliente = Cliente::where('ci_nit', '7894561')->firstOrFail();
    $pedido = Pedido::with('detalles')->latest('id')->firstOrFail();

    expect($pedido->cliente_id)->toBe($cliente->id)
        ->and($pedido->metodo_pago)->toBe('efectivo')
        ->and($pedido->tipo)->toBe('mesa')
        ->and($pedido->mesa)->toBe('Mesa 4')
        ->and((float) $pedido->total)->toBe(120.0)
        ->and($pedido->estado)->toBe(Pedido::ESTADO_PENDIENTE)
        ->and($pedido->detalles)->toHaveCount(2)
        ->and($cliente->nombre)->toBe('María')
        ->and($cliente->telefono)->toBe('70012345')
        ->and($cliente->registrado_por_user_id)->toBe($vendedor->id);
});

test('un cliente existente se reutiliza por su CI y el pago puede ser transferencia', function () {
    $vendedor = nuevoPedidoUser(Role::VENDEDOR);
    $cliente = Cliente::factory()->create(['ci_nit' => '1234567']);
    $plato = Plato::factory()->create(['precio' => 30]);

    $this->actingAs($vendedor)
        ->post(route('gestion.pedidos.store'), [
            'cliente_nombre' => 'Otro nombre',
            'cliente_ci_nit' => '1234567',
            'cliente_telefono' => '71111111',
            'tipo' => 'llevar',
            'metodo_pago' => 'transferencia',
            'platos' => [['plato_id' => $plato->id, 'cantidad' => 1]],
        ])
        ->assertSessionHasNoErrors();

    $pedido = Pedido::latest('id')->firstOrFail();

    expect($pedido->cliente_id)->toBe($cliente->id)
        ->and($pedido->metodo_pago)->toBe('transferencia')
        ->and($pedido->mesa)->toBeNull()
        ->and(Cliente::where('ci_nit', '1234567')->count())->toBe(1);
});

test('el formulario exige datos del cliente y al menos un plato', function () {
    $vendedor = nuevoPedidoUser(Role::VENDEDOR);

    $this->actingAs($vendedor)
        ->post(route('gestion.pedidos.store'), [
            'tipo' => 'llevar',
            'metodo_pago' => 'efectivo',
            'platos' => [],
        ])
        ->assertSessionHasErrors(['cliente_nombre', 'cliente_ci_nit', 'cliente_telefono', 'platos']);

    $this->assertDatabaseCount('pedidos', 0);
});
