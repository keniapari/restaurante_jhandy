<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['nombre', 'descripcion', 'categoria', 'precio', 'imagen', 'disponible', 'estado'])]
class Plato extends Model
{
    use HasFactory;

    public const CATEGORIAS = [
        'Entradas',
        'Platos fuertes',
        'Bebidas',
    ];

    protected function casts(): array
    {
        return [
            'precio' => 'decimal:2',
            'disponible' => 'boolean',
        ];
    }

    public function detalles(): HasMany
    {
        return $this->hasMany(PedidoDetalle::class);
    }

    public function scopeDisponibles($query)
    {
        return $query->where('estado', 'activo')->where('disponible', true);
    }
}
