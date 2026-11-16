<?php

namespace App\Http\Controllers;

use App\Models\Plato;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Inertia\Inertia;
use Inertia\Response;

class PlatosController extends Controller
{
    public function index(Request $request): Response
    {
        $platos = Plato::query()
            ->when($request->search, function ($query, $search) {
                $query->where(function ($query) use ($search) {
                    $query->where('nombre', 'like', "%{$search}%")
                        ->orWhere('categoria', 'like', "%{$search}%")
                        ->orWhere('descripcion', 'like', "%{$search}%");
                });
            })
            ->orderBy('categoria')
            ->orderBy('nombre')
            ->paginate(12)
            ->withQueryString();

        return Inertia::render('Platos/index', [
            'platos' => $platos,
            'categorias' => Plato::CATEGORIAS,
            'filters' => $request->only(['search']),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $this->validatePlato($request);

        Plato::create($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Plato registrado correctamente.']);

        return to_route('platos.index');
    }

    public function update(Request $request, Plato $plato): RedirectResponse
    {
        $validated = $this->validatePlato($request);

        $plato->update($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Plato actualizado correctamente.']);

        return to_route('platos.index');
    }

    public function toggleDisponibilidad(Request $request, Plato $plato): RedirectResponse
    {
        $validated = $request->validate([
            'disponible' => ['required', 'boolean'],
        ]);

        $plato->update(['disponible' => $validated['disponible']]);

        $estado = $plato->disponible ? 'disponible' : 'no disponible';
        Inertia::flash('toast', ['type' => 'success', 'message' => "El plato quedó {$estado}."]);

        return back();
    }

    public function destroy(Plato $plato): RedirectResponse
    {
        $plato->delete();

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Plato eliminado del menú.']);

        return to_route('platos.index');
    }

    /**
     * @return array{nombre: string, descripcion: string|null, categoria: string, precio: float, imagen: string|null, disponible: bool, estado: string}
     */
    private function validatePlato(Request $request): array
    {
        $validated = $request->validate([
            'nombre' => ['required', 'string', 'max:120'],
            'descripcion' => ['nullable', 'string', 'max:500'],
            'categoria' => ['required', 'string', Rule::in(Plato::CATEGORIAS)],
            'precio' => ['required', 'numeric', 'min:0', 'max:99999'],
            'imagen' => ['nullable', 'string', 'max:500'],
            'disponible' => ['boolean'],
            'estado' => ['required', 'string', Rule::in(['activo', 'inactivo'])],
        ]);

        $validated['nombre'] = trim($validated['nombre']);
        $validated['descripcion'] = isset($validated['descripcion']) ? trim($validated['descripcion']) : null;
        $validated['precio'] = (float) $validated['precio'];
        $validated['disponible'] = $request->boolean('disponible');
        $validated['estado'] = $validated['estado'] ?? 'activo';

        return $validated;
    }
}
