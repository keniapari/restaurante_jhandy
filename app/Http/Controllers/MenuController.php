<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use App\Models\ConfiguracionPago;
use App\Models\Plato;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Inertia\Inertia;
use Inertia\Response;

class MenuController extends Controller
{
    public function index(): Response
    {
        return Inertia::render('Menu/index', [
            'platos' => $this->platosDelMenu(),
            'categorias' => Plato::CATEGORIAS,
        ]);
    }

    public function welcome(): Response
    {
        return Inertia::render('Welcome', [
            'platos' => Plato::query()
                ->disponibles()
                ->orderBy('categoria')
                ->orderBy('nombre')
                ->limit(6)
                ->get(),
            'categorias' => Plato::CATEGORIAS,
        ]);
    }

    public function clienteIndex(): Response
    {
        $qrPago = ConfiguracionPago::actual()->qr_pago;

        /** @var FilesystemAdapter $discoPublico */
        $discoPublico = Storage::disk('public');

        return Inertia::render('Cliente/Menu', [
            'platos' => $this->platosDelMenu(),
            'categorias' => Plato::CATEGORIAS,
            'qrPagoUrl' => $qrPago ? $discoPublico->url((string) $qrPago) : null,
        ]);
    }

    public function conformar(): Response
    {
        return Inertia::render('Menu/conformar', [
            'platos' => $this->platosDelMenu(),
            'categorias' => Plato::CATEGORIAS,
            'clientes' => Cliente::query()
                ->where('estado', 'activo')
                ->orderBy('nombre')
                ->get(['id', 'nombre', 'apellido', 'ci_nit', 'telefono']),
        ]);
    }

    private function platosDelMenu(): mixed
    {
        return Plato::query()
            ->disponibles()
            ->orderBy('categoria')
            ->orderBy('nombre')
            ->get();
    }
}
