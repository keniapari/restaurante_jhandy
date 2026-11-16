<?php

use App\Models\Cliente;
use App\Models\ConfiguracionPago;
use App\Models\Pedido;
use App\Models\Role;
use App\Models\User;
use Database\Seeders\PermissionsSeeder;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(fn () => $this->seed(PermissionsSeeder::class));

function usuarioTransferencia(string $rol): User
{
    $user = User::factory()->create(['role' => $rol]);
    $role = Role::where('nombre', $rol)->firstOrFail();
    $user->roles()->sync([$role->id]);

    return $user->fresh();
}

function pedidoTransferencia(User $user, Cliente $cliente): Pedido
{
    return Pedido::create([
        'numero' => 'PED-'.fake()->unique()->numerify('########'),
        'user_id' => $user->id,
        'cliente_id' => $cliente->id,
        'total' => 25,
        'estado' => Pedido::ESTADO_PENDIENTE,
        'tipo' => 'llevar',
        'metodo_pago' => 'transferencia',
    ]);
}

test('la propietaria puede guardar el QR de transferencia', function () {
    Storage::fake('public');
    $propietaria = usuarioTransferencia(Role::ADMIN);

    $response = $this->actingAs($propietaria)->post(route('configuracion.pagos.update'), [
        'qr_pago' => UploadedFile::fake()->image('qr.png'),
    ]);

    $response->assertRedirect(route('configuracion.pagos.edit'))->assertSessionHasNoErrors();

    $rutaQr = ConfiguracionPago::actual()->qr_pago;

    expect($rutaQr)->not->toBeNull();
    Storage::disk('public')->assertExists($rutaQr);

    $this->actingAs($propietaria)
        ->get(route('configuracion.pagos.edit'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Configuracion/Pagos')
            ->where('qrPagoUrl', Storage::disk('public')->url($rutaQr)));
});

test('la propietaria debe subir un QR o indicar que quiere eliminarlo', function () {
    $propietaria = usuarioTransferencia(Role::ADMIN);

    $this->actingAs($propietaria)
        ->post(route('configuracion.pagos.update'))
        ->assertSessionHasErrors('qr_pago');
});

test('el QR configurado se muestra en la carta del cliente', function () {
    Storage::fake('public');
    $clienteUsuario = usuarioTransferencia(Role::CLIENTE);
    $rutaQr = UploadedFile::fake()->image('qr.png')->store('pagos', 'public');
    ConfiguracionPago::create(['qr_pago' => $rutaQr]);

    $this->actingAs($clienteUsuario)
        ->get(route('cliente.menu.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('Cliente/Menu')
            ->where('qrPagoUrl', Storage::disk('public')->url($rutaQr)));
});

test('el cliente puede adjuntar un comprobante a su pedido por transferencia', function () {
    Storage::fake('public');
    $user = usuarioTransferencia(Role::CLIENTE);
    $cliente = $user->cliente()->create([
        'nombre' => $user->name,
        'email' => $user->email,
        'estado' => 'activo',
    ]);
    $pedido = pedidoTransferencia($user, $cliente);

    $response = $this->actingAs($user)->post(
        route('perfil.pedidos.comprobante', $pedido),
        ['comprobante' => UploadedFile::fake()->image('transferencia.png')],
    );

    $response->assertRedirect(route('perfil'))->assertSessionHasNoErrors();

    $rutaComprobante = $pedido->fresh()->comprobante_pago;

    expect($rutaComprobante)->not->toBeNull();
    Storage::disk('public')->assertExists($rutaComprobante);
});

test('el cliente no puede subir un comprobante a un pedido de otra persona', function () {
    $user = usuarioTransferencia(Role::CLIENTE);
    $owner = usuarioTransferencia(Role::CLIENTE);
    $cliente = $owner->cliente()->create([
        'nombre' => $owner->name,
        'email' => $owner->email,
        'estado' => 'activo',
    ]);
    $pedido = pedidoTransferencia($owner, $cliente);

    $this->actingAs($user)
        ->post(route('perfil.pedidos.comprobante', $pedido), [
            'comprobante' => UploadedFile::fake()->image('transferencia.png'),
        ])
        ->assertNotFound();
});
