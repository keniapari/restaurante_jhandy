<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use App\Models\Pedido;
use App\Models\Plato;
use App\Models\Role;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Inertia\Inertia;

class PedidosController extends Controller
{
    /**
     * Registra un pedido realizado por un cliente desde la carta.
     */
    public function storeCliente(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'observaciones' => ['nullable', 'string', 'max:500'],
            'platos' => ['required', 'array', 'min:1'],
            'platos.*.plato_id' => ['required', 'integer', 'exists:platos,id'],
            'platos.*.cantidad' => ['required', 'integer', 'min:1', 'max:50'],
        ]);

        $user = $request->user();
        $cliente = $user->cliente()->firstOrCreate(
            [],
            [
                'nombre' => $user->name,
                'email' => $user->email,
                'telefono' => $user->telefono,
                'estado' => 'activo',
            ],
        );

        $validated['cliente_id'] = $cliente->id;
        $validated['tipo'] = 'llevar';
        $validated['metodo_pago'] = 'transferencia';

        return $this->registrarPedido($request, $validated);
    }

    /**
     * Registra un pedido de restaurante desde el formulario de nuevo pedido.
     */
    public function storeNuevo(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'cliente_nombre' => ['required', 'string', 'max:160'],
            'cliente_apellido' => ['nullable', 'string', 'max:160'],
            'cliente_ci_nit' => ['required', 'string', 'max:20'],
            'cliente_telefono' => ['required', 'string', 'max:30'],
            'tipo' => ['required', 'string', 'in:mesa,llevar'],
            'mesa' => ['nullable', 'string', 'max:20', 'required_if:tipo,mesa'],
            'metodo_pago' => ['required', 'string', 'in:efectivo,transferencia'],
            'observaciones' => ['nullable', 'string', 'max:500'],
            'platos' => ['required', 'array', 'min:1'],
            'platos.*.plato_id' => ['required', 'integer', 'exists:platos,id'],
            'platos.*.cantidad' => ['required', 'integer', 'min:1', 'max:50'],
        ]);

        return $this->registrarPedido($request, $validated);
    }

    /**
     * Registra un pedido de restaurante a partir de los platos seleccionados en el menú.
     */
    public function storeRestaurante(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'cliente_id' => ['nullable', 'integer', 'exists:clientes,id'],
            'cliente_nombre' => ['nullable', 'string', 'max:160'],
            'cliente_apellido' => ['nullable', 'string', 'max:160'],
            'cliente_ci_nit' => ['nullable', 'string', 'max:20'],
            'cliente_telefono' => ['nullable', 'string', 'max:30'],
            'tipo' => ['required', 'string', 'in:mesa,llevar'],
            'mesa' => ['nullable', 'string', 'max:20', 'required_if:tipo,mesa'],
            'metodo_pago' => ['nullable', 'string', 'in:efectivo,transferencia'],
            'observaciones' => ['nullable', 'string', 'max:500'],
            'platos' => ['required', 'array', 'min:1'],
            'platos.*.plato_id' => ['required', 'integer', 'exists:platos,id'],
            'platos.*.cantidad' => ['required', 'integer', 'min:1', 'max:50'],
        ]);

        return $this->registrarPedido($request, $validated);
    }

    /**
     * @param  array<string, mixed>  $validated
     */
    private function registrarPedido(Request $request, array $validated): RedirectResponse
    {
        try {
            $pedido = DB::transaction(function () use ($request, $validated): Pedido {
                $clienteId = $validated['cliente_id'] ?? null;

                if (! $clienteId && filled($validated['cliente_ci_nit'] ?? null)) {
                    $cliente = Cliente::query()->firstOrCreate(
                        ['ci_nit' => $validated['cliente_ci_nit']],
                        [
                            'nombre' => $validated['cliente_nombre'],
                            'apellido' => $validated['cliente_apellido'] ?? null,
                            'telefono' => $validated['cliente_telefono'] ?? null,
                            'estado' => 'activo',
                            'registrado_por_user_id' => $request->user()->id,
                        ],
                    );

                    $clienteId = $cliente->id;
                }

                $pedido = Pedido::create([
                    'numero' => $this->generarNumero(),
                    'user_id' => $request->user()->id,
                    'cliente_id' => $clienteId,
                    'total' => 0,
                    'estado' => Pedido::ESTADO_PENDIENTE,
                    'tipo' => $validated['tipo'],
                    'mesa' => $validated['tipo'] === 'mesa' ? $validated['mesa'] ?? null : null,
                    'observaciones' => $validated['observaciones'] ?? null,
                    'metodo_pago' => $validated['metodo_pago'] ?? 'efectivo',
                ]);

                $total = 0.0;

                foreach ($validated['platos'] as $item) {
                    $plato = Plato::query()
                        ->disponibles()
                        ->find($item['plato_id']);

                    if (! $plato) {
                        throw ValidationException::withMessages([
                            'platos' => 'Uno de los platos seleccionados ya no está disponible.',
                        ]);
                    }

                    $precio = (float) $plato->precio;
                    $subtotal = $precio * $item['cantidad'];

                    $pedido->detalles()->create([
                        'plato_id' => $plato->id,
                        'producto' => $plato->nombre,
                        'cantidad' => $item['cantidad'],
                        'precio' => $precio,
                        'subtotal' => $subtotal,
                        'imagen' => $plato->imagen,
                    ]);

                    $total += $subtotal;
                }

                $pedido->update(['total' => $total]);

                return $pedido->fresh('detalles');
            }, 3);

            Inertia::flash('toast', [
                'type' => 'success',
                'message' => "Pedido {$pedido->numero} registrado correctamente.",
            ]);

            if ($request->user()->hasRole(Role::CLIENTE)) {
                return to_route('perfil');
            }

            return to_route('gestion.pedidos.show', $pedido);
        } catch (ValidationException $e) {
            throw $e;
        } catch (\Exception $e) {
            return back()->withErrors(['pedido' => 'Error al registrar el pedido: '.$e->getMessage()]);
        }
    }

    private function generarNumero(): string
    {
        $numero = 'PED-'.now()->format('Ymd').'-'.str_pad((Pedido::max('id') ?? 0) + 1, 4, '0', STR_PAD_LEFT);

        while (Pedido::where('numero', $numero)->exists()) {
            $numero = 'PED-'.now()->format('Ymd').'-'.str_pad(mt_rand(1, 9999), 4, '0', STR_PAD_LEFT);
        }

        return $numero;
    }
}
