<?php

use App\Http\Controllers\Auth\GoogleAuthController;
use App\Http\Controllers\ClientesController;
use App\Http\Controllers\ConfiguracionPagoController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\MenuController;
use App\Http\Controllers\PedidosController;
use App\Http\Controllers\PedidosGestionController;
use App\Http\Controllers\PerfilController;
use App\Http\Controllers\PlatosController;
use App\Http\Controllers\ReportesController;
use App\Http\Controllers\ReservasController;
use App\Http\Controllers\RolesController;
use App\Http\Controllers\UsersController;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    $user = Auth::user();

    if (! $user) {
        return app(MenuController::class)->welcome();
    }

    if ($user->hasRole('cliente')) {
        return redirect()->route('cliente.menu.index');
    }

    return redirect()->route('dashboard');
})->name('principal');

Route::middleware(['guest', 'throttle:10,1'])->group(function () {
    Route::get('auth/google/redirect', [GoogleAuthController::class, 'redirect'])->name('auth.google.redirect');
    Route::get('auth/google/callback', [GoogleAuthController::class, 'callback'])->name('auth.google.callback');
});

Route::middleware(['auth', 'verified', 'role:admin'])
    ->prefix('configuracion')
    ->name('configuracion.')
    ->group(function () {
        Route::get('pagos', [ConfiguracionPagoController::class, 'edit'])->name('pagos.edit');
        Route::post('pagos', [ConfiguracionPagoController::class, 'update'])->name('pagos.update');
    });

Route::middleware(['auth', 'verified', 'role:cliente'])->group(function () {
    Route::get('perfil', [PerfilController::class, 'index'])->name('perfil');
    Route::patch('perfil', [PerfilController::class, 'update'])->name('perfil.update');
    Route::post('perfil/pedidos/{pedido}/comprobante', [PerfilController::class, 'subirComprobante'])
        ->name('perfil.pedidos.comprobante');

    Route::get('carta', [MenuController::class, 'clienteIndex'])->name('cliente.menu.index');
    Route::post('carta/pedido', [PedidosController::class, 'storeCliente'])->name('cliente.menu.store');
});

Route::middleware(['auth', 'verified', 'redirect-client', 'role:admin,vendedor,encargado_inventario', 'permission:pedidos.ver'])
    ->prefix('gestion')
    ->name('gestion.')
    ->group(function () {
        Route::get('pedidos', [PedidosGestionController::class, 'index'])->name('pedidos.index');
        Route::get('pedidos/create', [PedidosGestionController::class, 'create'])
            ->middleware('permission:pedidos.crear')
            ->name('pedidos.create');
        Route::get('pedidos/{pedido}', [PedidosGestionController::class, 'show'])->name('pedidos.show');

        Route::middleware('permission:pedidos.crear')->group(function () {
            Route::post('pedidos', [PedidosController::class, 'storeNuevo'])->name('pedidos.store');
        });

        Route::post('pedidos/{pedido}/confirmar', [PedidosGestionController::class, 'confirmar'])
            ->middleware('permission:pedidos.confirmar')
            ->name('pedidos.confirmar');

        Route::middleware('permission:pedidos.cocina')->group(function () {
            Route::post('pedidos/{pedido}/preparar', [PedidosGestionController::class, 'preparar'])->name('pedidos.preparar');
            Route::post('pedidos/{pedido}/listo', [PedidosGestionController::class, 'listo'])->name('pedidos.listo');
        });

        Route::middleware('permission:pedidos.gestion')->group(function () {
            Route::patch('pedidos/{pedido}/estado', [PedidosGestionController::class, 'updateEstado'])->name('pedidos.estado');
            Route::post('pedidos/{pedido}/entregar', [PedidosGestionController::class, 'entregar'])->name('pedidos.entregar');
            Route::post('pedidos/{pedido}/cancelar', [PedidosGestionController::class, 'cancelar'])->name('pedidos.cancelar');
        });
    });

Route::middleware(['auth', 'verified', 'redirect-client', 'role:admin,vendedor', 'permission:menu.ver'])
    ->prefix('menu')
    ->name('menu.')
    ->group(function () {
        Route::get('/', [MenuController::class, 'index'])->name('index');
        Route::get('conformar', [MenuController::class, 'conformar'])->name('conformar');
        Route::post('conformar', [PedidosController::class, 'storeRestaurante'])
            ->middleware('permission:pedidos.crear')
            ->name('conformar.store');
    });

Route::middleware(['auth', 'verified', 'redirect-client', 'role:admin,vendedor,encargado_inventario'])
    ->prefix('platos')
    ->name('platos.')
    ->group(function () {
        Route::get('/', [PlatosController::class, 'index'])
            ->middleware('permission:platos.ver')
            ->name('index');

        Route::middleware('permission:platos.gestion')->group(function () {
            Route::post('/', [PlatosController::class, 'store'])->name('store');
            Route::patch('{plato}', [PlatosController::class, 'update'])->name('update');
            Route::patch('{plato}/disponibilidad', [PlatosController::class, 'toggleDisponibilidad'])->name('disponibilidad.update');
            Route::delete('{plato}', [PlatosController::class, 'destroy'])->name('destroy');
        });
    });

Route::middleware(['auth', 'verified', 'redirect-client', 'role:admin,vendedor'])
    ->prefix('reservas')
    ->name('reservas.')
    ->group(function () {
        Route::get('/', [ReservasController::class, 'index'])
            ->middleware('permission:reservas.ver')
            ->name('index');

        Route::middleware('permission:reservas.gestion')->group(function () {
            Route::post('/', [ReservasController::class, 'store'])->name('store');
            Route::patch('{reserva}', [ReservasController::class, 'update'])->name('update');
            Route::patch('{reserva}/estado', [ReservasController::class, 'updateEstado'])->name('estado');
            Route::delete('{reserva}', [ReservasController::class, 'destroy'])->name('destroy');
        });
    });

Route::middleware(['auth', 'verified', 'redirect-client', 'role:admin,vendedor,encargado_inventario'])->group(function () {
    Route::get('dashboard', DashboardController::class)
        ->middleware('permission:panel.ver')
        ->name('dashboard');
});

Route::middleware(['auth', 'redirect-client'])->group(function () {
    Route::prefix('clientes')
        ->name('clientes.')
        ->middleware('permission:clientes.ver')
        ->group(function () {
            Route::get('/', [ClientesController::class, 'index'])->name('index');
            Route::get('{cliente}', [ClientesController::class, 'show'])->name('show');

            Route::middleware('permission:clientes.gestion')->group(function () {
                Route::post('/', [ClientesController::class, 'store'])->name('store');
                Route::patch('{cliente}', [ClientesController::class, 'update'])->name('update');
                Route::patch('{cliente}/estado', [ClientesController::class, 'toggleEstado'])->name('estado');
            });
        });
});

Route::middleware(['auth', 'redirect-client'])->group(function () {
    Route::prefix('reportes')
        ->name('reportes.')
        ->middleware('permission:panel.ver')
        ->group(function () {
            Route::middleware('permission:reportes.compras.ver')->group(function () {
                Route::get('/', [ReportesController::class, 'compras'])->name('index');
                Route::get('compras', [ReportesController::class, 'compras'])->name('compras');
                Route::get('compras/vista-pdf', [ReportesController::class, 'comprasVistaPdf'])->name('compras.vista-pdf');
                Route::get('compras/pdf', [ReportesController::class, 'comprasPdf'])->name('compras.pdf');
            });

            Route::middleware('permission:reportes.ventas.ver')->group(function () {
                Route::get('ventas', [ReportesController::class, 'ventas'])->name('ventas');
                Route::get('ventas/vista-pdf', [ReportesController::class, 'ventasVistaPdf'])->name('ventas.vista-pdf');
                Route::get('ventas/pdf', [ReportesController::class, 'ventasPdf'])->name('ventas.pdf');
            });
        });
});

Route::middleware(['auth', 'verified', 'role:admin', 'permission:usuarios.gestion'])->group(function () {
    Route::resource('roles', RolesController::class)->except(['show', 'create', 'edit']);

    Route::prefix('usuarios')->name('usuarios.')->group(function () {
        Route::get('/', [UsersController::class, 'index'])->name('index');
        Route::post('/', [UsersController::class, 'store'])->name('store');
        Route::patch('{user}', [UsersController::class, 'update'])->name('update');
        Route::delete('{user}', [UsersController::class, 'destroy'])->name('destroy');
        Route::patch('{user}/status', [UsersController::class, 'toggleStatus'])->name('toggle-status');
    });
});

Route::get('configuraciones', fn () => redirect()->route('profile.edit'))
    ->middleware(['auth', 'verified', 'role:admin', 'permission:configuraciones.gestion'])
    ->name('configuraciones.index');

require __DIR__.'/settings.php';
