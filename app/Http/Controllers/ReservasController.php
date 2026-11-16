<?php

namespace App\Http\Controllers;

use App\Models\Reserva;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Inertia\Inertia;
use Inertia\Response;

class ReservasController extends Controller
{
    public function index(Request $request): Response
    {
        $reservas = Reserva::query()
            ->with('cliente:id,nombre,apellido,ci_nit')
            ->when($request->search, function ($query, $search) {
                $query->where(function ($query) use ($search) {
                    $query->where('nombre_cliente', 'like', "%{$search}%")
                        ->orWhere('telefono', 'like', "%{$search}%")
                        ->orWhere('mesa', 'like', "%{$search}%")
                        ->orWhere('tipo_evento', 'like', "%{$search}%")
                        ->orWhere('estado', 'like', "%{$search}%");
                });
            })
            ->orderByDesc('fecha')
            ->orderByDesc('hora')
            ->paginate(10)
            ->withQueryString();

        return Inertia::render('Reservas/index', [
            'reservas' => $reservas,
            'estados' => Reserva::ESTADOS,
            'tiposEvento' => Reserva::TIPOS_EVENTO,
            'metodosPago' => Reserva::METODOS_PAGO,
            'filters' => $request->only(['search']),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $this->validateReserva($request);

        Reserva::create([
            ...$validated,
            'user_id' => $request->user()->id,
        ]);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Reserva registrada correctamente.']);

        return to_route('reservas.index');
    }

    public function update(Request $request, Reserva $reserva): RedirectResponse
    {
        $validated = $this->validateReserva($request);

        $reserva->update($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Reserva actualizada correctamente.']);

        return to_route('reservas.index');
    }

    public function updateEstado(Request $request, Reserva $reserva): RedirectResponse
    {
        $validated = $request->validate([
            'estado' => ['required', 'string', Rule::in(Reserva::ESTADOS)],
        ]);

        $reserva->update(['estado' => $validated['estado']]);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Estado de la reserva actualizado.']);

        return back();
    }

    public function destroy(Reserva $reserva): RedirectResponse
    {
        $reserva->delete();

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Reserva eliminada.']);

        return to_route('reservas.index');
    }

    /**
     * @return array{cliente_id: int|null, nombre_cliente: string, telefono: string|null, fecha: string, hora: string, personas: int, tipo_evento: string, cantidad_platos: int, metodo_pago: string, mesa: string|null, estado: string, observaciones: string|null}
     */
    private function validateReserva(Request $request): array
    {
        $validated = $request->validate([
            'cliente_id' => ['nullable', 'integer', 'exists:clientes,id'],
            'nombre_cliente' => ['required', 'string', 'max:160'],
            'telefono' => ['nullable', 'string', 'max:30'],
            'fecha' => ['required', 'date', 'after_or_equal:today'],
            'hora' => ['required', 'date_format:H:i'],
            'personas' => ['required', 'integer', 'min:1', 'max:50'],
            'tipo_evento' => ['required', 'string', Rule::in(array_keys(Reserva::TIPOS_EVENTO))],
            'cantidad_platos' => ['required', 'integer', 'min:11', 'max:500'],
            'metodo_pago' => ['required', 'string', Rule::in(array_keys(Reserva::METODOS_PAGO))],
            'mesa' => ['nullable', 'string', 'max:20'],
            'estado' => ['required', 'string', Rule::in(Reserva::ESTADOS)],
            'observaciones' => ['nullable', 'string', 'max:500'],
        ]);

        $validated['nombre_cliente'] = trim($validated['nombre_cliente']);
        $validated['cliente_id'] = $validated['cliente_id'] ?? null;
        $validated['telefono'] = isset($validated['telefono']) ? trim($validated['telefono']) : null;
        $validated['mesa'] = isset($validated['mesa']) ? trim($validated['mesa']) : null;
        $validated['observaciones'] = isset($validated['observaciones']) ? trim($validated['observaciones']) : null;

        return $validated;
    }
}
