<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['cliente_id', 'user_id', 'nombre_cliente', 'telefono', 'fecha', 'hora', 'personas', 'tipo_evento', 'cantidad_platos', 'metodo_pago', 'mesa', 'estado', 'observaciones'])]
class Reserva extends Model
{
    use HasFactory;

    public const ESTADOS = [
        'pendiente',
        'confirmada',
        'completada',
        'cancelada',
    ];

    public const TIPOS_EVENTO = [
        'reunion' => 'Reunión',
        'cumpleanos' => 'Cumpleaños',
        'otra_festividad' => 'Otra festividad',
    ];

    public const METODOS_PAGO = [
        'efectivo' => 'Efectivo',
        'transferencia' => 'Transferencia',
    ];

    protected function casts(): array
    {
        return [
            'fecha' => 'date',
            'personas' => 'integer',
            'cantidad_platos' => 'integer',
        ];
    }

    public function cliente(): BelongsTo
    {
        return $this->belongsTo(Cliente::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
