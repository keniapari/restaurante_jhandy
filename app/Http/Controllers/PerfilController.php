<?php

namespace App\Http\Controllers;

use App\Models\ConfiguracionPago;
use App\Models\Pedido;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Validation\Rule;
use Inertia\Inertia;
use Inertia\Response;
use RuntimeException;

class PerfilController extends Controller
{
    public function index(Request $request): Response
    {
        $cliente = $request->user()->cliente;
        $qrPago = ConfiguracionPago::actual()->qr_pago;

        return Inertia::render('Perfil/index', [
            'mustVerifyEmail' => $request->user() instanceof MustVerifyEmail,
            'status' => $request->session()->get('status'),
            'cliente' => $cliente,
            'qrPagoUrl' => $qrPago ? Storage::disk('public')->url((string) $qrPago) : null,
            'pedidos' => $cliente
                ? $cliente->pedidos()
                    ->with('detalles')
                    ->latest()
                    ->limit(20)
                    ->get()
                    ->map(fn ($pedido) => $pedido->toClienteArray())
                    ->all()
                : [],
        ]);
    }

    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        $validated = $request->validate([
            'nombres' => 'required|string|max:255',
            'apellido_paterno' => 'required|string|max:255',
            'apellido_materno' => 'required|string|max:255',
            'telefono' => 'nullable|string|max:20',
            'email' => "required|email|max:255|unique:users,email,{$user->id}",
            'ci_nit' => [
                'nullable',
                'string',
                'max:20',
                Rule::unique('clientes', 'ci_nit')->ignore($user->cliente?->id),
            ],
            'direccion' => ['nullable', 'string', 'max:500'],
        ]);

        $user->fill($validated);

        if ($user->isDirty('email')) {
            $user->email_verified_at = null;
        }

        $user->save();

        $user->cliente()->updateOrCreate(
            [],
            [
                'nombre' => trim(implode(' ', array_filter([
                    $validated['nombres'],
                    $validated['apellido_paterno'],
                    $validated['apellido_materno'],
                ]))),
                'apellido' => null,
                'email' => $validated['email'],
                'telefono' => $validated['telefono'] ?? null,
                'ci_nit' => $validated['ci_nit'] ?? null,
                'direccion' => $validated['direccion'] ?? null,
                'estado' => 'activo',
            ],
        );

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Perfil actualizado exitosamente.']);

        return to_route('perfil');
    }

    public function subirComprobante(Request $request, Pedido $pedido): RedirectResponse
    {
        $validated = $request->validate([
            'comprobante' => ['required', 'file', 'mimes:jpg,jpeg,png,webp,pdf', 'max:5120'],
        ]);

        $cliente = $request->user()->cliente;

        abort_unless($cliente, 404);

        $pedido = $cliente->pedidos()->findOrFail($pedido->id);

        abort_unless($pedido->metodo_pago === 'transferencia', 404);

        $rutaAnterior = $pedido->comprobante_pago;
        $ruta = $validated['comprobante']->store('comprobantes-pago', 'public');

        if (! $ruta) {
            throw new RuntimeException('No se pudo guardar el comprobante de pago.');
        }

        $pedido->update(['comprobante_pago' => $ruta]);

        if ($rutaAnterior) {
            Storage::disk('public')->delete($rutaAnterior);
        }

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Comprobante enviado correctamente.']);

        return to_route('perfil');
    }
}
