<?php

namespace App\Http\Controllers;

use App\Models\ConfiguracionPago;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Inertia\Inertia;
use Inertia\Response;
use RuntimeException;

class ConfiguracionPagoController extends Controller
{
    public function edit(): Response
    {
        $qrPago = ConfiguracionPago::actual()->qr_pago;

        return Inertia::render('Configuracion/Pagos', [
            'qrPagoUrl' => $qrPago ? Storage::disk('public')->url((string) $qrPago) : null,
        ]);
    }

    public function update(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'qr_pago' => [
                'required_without:eliminar_qr',
                'nullable',
                'image',
                'mimes:jpg,jpeg,png,webp',
                'max:4096',
            ],
            'eliminar_qr' => ['nullable', 'boolean'],
        ]);

        $configuracion = ConfiguracionPago::actual();

        if (isset($validated['qr_pago'])) {
            $rutaAnterior = $configuracion->qr_pago;
            $ruta = $validated['qr_pago']->store('pagos', 'public');

            if (! $ruta) {
                throw new RuntimeException('No se pudo guardar el código QR de pago.');
            }

            $configuracion->update(['qr_pago' => $ruta]);

            if ($rutaAnterior) {
                Storage::disk('public')->delete($rutaAnterior);
            }
        } elseif (($validated['eliminar_qr'] ?? false) && $configuracion->qr_pago) {
            Storage::disk('public')->delete($configuracion->qr_pago);
            $configuracion->update(['qr_pago' => null]);
        }

        Inertia::flash('toast', ['type' => 'success', 'message' => 'QR de pago actualizado correctamente.']);

        return to_route('configuracion.pagos.edit');
    }
}
