<?php

use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Reserva;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

test('guests are redirected to the login page', function () {
    $response = $this->get(route('dashboard'));
    $response->assertRedirect(route('login'));
});

test('authenticated users can visit the dashboard', function () {
    $this->seed(PermissionsSeeder::class);
    $user = User::factory()->create(['role' => 'vendedor']);
    $user->assignRole('vendedor');

    $response = $this
        ->actingAs($user)
        ->get(route('dashboard'));

    $response->assertOk();
});

test('dashboard shows restaurant statistics from real data', function () {
    $this->seed(PermissionsSeeder::class);
    $user = User::factory()->create(['role' => 'admin']);
    $user->assignRole('admin');

    Cliente::create([
        'nombre' => 'Maria',
        'apellido' => 'Perez',
        'email' => 'maria@example.com',
        'telefono' => '77777777',
        'direccion' => 'Calle Falsa 123',
        'ci_nit' => '1234567',
    ]);

    Plato::factory()->count(2)->create();
    Plato::factory()->noDisponible()->create();

    Reserva::factory()->create(['estado' => 'pendiente']);

    Pedido::create([
        'numero' => 'PED-DASHBOARD-0001',
        'user_id' => $user->id,
        'total' => 150.00,
        'estado' => Pedido::ESTADO_PENDIENTE,
        'tipo' => 'mesa',
        'mesa' => '4',
    ]);

    $response = $this
        ->actingAs($user)
        ->get(route('dashboard'));

    $response
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Dashboard')
            ->where('stats.totalUsuarios', 1)
            ->where('stats.totalClientes', 1)
            ->where('stats.totalPlatos', 3)
            ->where('stats.platosDisponibles', 2)
            ->where('stats.totalPedidos', 1)
            ->where('stats.pedidosPendientes', 1)
            ->where('stats.pedidosHoy', 1)
            ->where('stats.ventasHoy', 150)
            ->where('stats.ventasMes', 150)
            ->where('stats.totalReservas', 1)
            ->where('stats.reservasPendientes', 1));
});
