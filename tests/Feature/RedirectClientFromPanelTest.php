<?php

use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function userCliente(): User
{
    $role = Role::firstOrCreate(
        ['nombre' => Role::CLIENTE],
        ['descripcion' => 'Cliente del restaurante']
    );
    $user = User::factory()->create(['role' => Role::CLIENTE]);
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

test('invitado en / ve el menu', function () {
    $this->get('/')->assertOk();
});

test('cliente autenticado en / es redirigido a su perfil', function () {
    $user = userCliente();

    $this->actingAs($user)->get('/')->assertRedirect(route('cliente.menu.index'));
});

test('cliente autenticado en /dashboard es redirigido a su perfil', function () {
    $user = userCliente();

    $this->actingAs($user)->get(route('dashboard'))->assertRedirect(route('cliente.menu.index'));
});

test('cliente autenticado en reportes es redirigido a su perfil', function () {
    $user = userCliente();

    $this->actingAs($user)->get(route('reportes.index'))->assertRedirect(route('cliente.menu.index'));
});

test('admin en / es redirigido al dashboard', function () {
    $user = User::factory()->create(['role' => Role::ADMIN]);
    $role = Role::where('nombre', Role::ADMIN)->firstOrFail();
    $user->roles()->sync([$role->id]);

    $this->actingAs($user)->get('/')->assertRedirect(route('dashboard'));
});

test('admin en /dashboard no es redirigido', function () {
    $user = User::factory()->create(['role' => Role::ADMIN]);
    $role = Role::where('nombre', Role::ADMIN)->firstOrFail();
    $user->roles()->sync([$role->id]);

    $this->actingAs($user)->get(route('dashboard'))->assertOk();
});
