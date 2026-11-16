<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Reserva;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;
use Inertia\Response;

class DashboardController extends Controller
{
    public function __invoke(): Response
    {
        $user = Auth::user();

        $pedidosValidos = Pedido::query()
            ->where('estado', '!=', Pedido::ESTADO_CANCELADO);

        $ventasHoy = (float) (clone $pedidosValidos)
            ->whereDate('created_at', today())
            ->sum('total');
        $ventasMes = (float) (clone $pedidosValidos)
            ->whereBetween('created_at', [now()->startOfMonth(), now()->endOfMonth()])
            ->sum('total');

        $isVendedor = $user && $user->hasRole('vendedor');

        return Inertia::render('Dashboard', [
            'stats' => [
                'totalUsuarios' => User::count(),
                'totalClientes' => Cliente::count(),
                'totalPlatos' => Plato::count(),
                'platosDisponibles' => Plato::query()->disponibles()->count(),
                'totalPedidos' => Pedido::count(),
                'pedidosPendientes' => Pedido::query()
                    ->whereIn('estado', [Pedido::ESTADO_PENDIENTE, Pedido::ESTADO_CONFIRMADO, Pedido::ESTADO_EN_PREPARACION])
                    ->count(),
                'pedidosHoy' => Pedido::query()->whereDate('created_at', today())->count(),
                'ventasHoy' => $ventasHoy,
                'ventasMes' => $ventasMes,
                'totalReservas' => Reserva::count(),
                'reservasPendientes' => Reserva::query()->where('estado', 'pendiente')->count(),
            ],
            'isVendedor' => $isVendedor,
        ]);
    }
}
