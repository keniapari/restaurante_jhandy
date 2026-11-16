<?php

use App\Models\Plato;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function restaurantePlatosUser(string $roleName): User
{
    $user = User::factory()->create(['role' => $roleName]);
    $role = Role::where('nombre', $roleName)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

function restaurantePlatoPayload(array $overrides = []): array
{
    return array_merge([
        'nombre' => 'Silpancho',
        'descripcion' => 'Carne apanada con arroz y papa.',
        'categoria' => 'Platos fuertes',
        'precio' => 35,
        'imagen' => '/images/restaurant/plato-1.jpg',
        'disponible' => true,
        'estado' => 'activo',
    ], $overrides);
}

test('admin puede listar y registrar platos', function () {
    $admin = restaurantePlatosUser(Role::ADMIN);

    $this->actingAs($admin)
        ->get(route('platos.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Platos/index')
            ->has('platos.data')
            ->has('categorias'));

    $this->actingAs($admin)
        ->post(route('platos.store'), restaurantePlatoPayload())
        ->assertRedirect(route('platos.index'))
        ->assertSessionHasNoErrors();

    expect(Plato::where('nombre', 'Silpancho')->exists())->toBeTrue();
});

test('vendedor puede ver platos pero no registrarlos', function () {
    $vendedor = restaurantePlatosUser(Role::VENDEDOR);

    $this->actingAs($vendedor)->get(route('platos.index'))->assertOk();

    $this->actingAs($vendedor)
        ->post(route('platos.store'), restaurantePlatoPayload())
        ->assertForbidden();
});

test('encargado de inventario puede ver platos', function () {
    $encargado = restaurantePlatosUser(Role::ENCARGADO_INVENTARIO);

    $this->actingAs($encargado)->get(route('platos.index'))->assertOk();
});

test('admin puede actualizar disponibilidad y editar un plato', function () {
    $admin = restaurantePlatosUser(Role::ADMIN);
    $plato = Plato::factory()->create(['disponible' => true]);

    $this->actingAs($admin)
        ->patch(route('platos.disponibilidad.update', $plato), ['disponible' => false])
        ->assertRedirect();

    expect($plato->fresh()->disponible)->toBeFalse();

    $this->actingAs($admin)
        ->patch(route('platos.update', $plato), restaurantePlatoPayload(['nombre' => 'Pique macho', 'precio' => 55]))
        ->assertRedirect(route('platos.index'))
        ->assertSessionHasNoErrors();

    expect($plato->fresh()->nombre)->toBe('Pique macho')
        ->and((float) $plato->fresh()->precio)->toBe(55.0);
});

test('admin puede eliminar un plato', function () {
    $admin = restaurantePlatosUser(Role::ADMIN);
    $plato = Plato::factory()->create();

    $this->actingAs($admin)
        ->delete(route('platos.destroy', $plato))
        ->assertRedirect(route('platos.index'));

    $this->assertDatabaseMissing('platos', ['id' => $plato->id]);
});

test('la categoria del plato debe ser valida', function () {
    $admin = restaurantePlatosUser(Role::ADMIN);

    $this->actingAs($admin)
        ->post(route('platos.store'), restaurantePlatoPayload(['categoria' => 'Sushi']))
        ->assertSessionHasErrors('categoria');

    $this->assertDatabaseCount('platos', 0);
});
