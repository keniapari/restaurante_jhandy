<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

#[Fillable(['numero', 'user_id', 'cliente_id', 'venta_id', 'total', 'estado', 'tipo', 'mesa', 'observaciones', 'metodo_pago', 'comprobante_pago'])]
class Pedido extends Model
{
    public const ESTADOS = [
        'Pendiente',
        'Confirmado',
        'En preparación',
        'Listo',
        'Enviado',
        'Entregado',
        'Cancelado',
    ];

    public const ESTADO_PENDIENTE = 'Pendiente';

    public const ESTADO_CONFIRMADO = 'Confirmado';

    public const ESTADO_EN_PREPARACION = 'En preparación';

    public const ESTADO_LISTO = 'Listo';

    public const ESTADO_ENVIADO = 'Enviado';

    public const ESTADO_ENTREGADO = 'Entregado';

    public const ESTADO_CANCELADO = 'Cancelado';

    protected function casts(): array
    {
        return [
            'total' => 'decimal:2',
            'created_at' => 'datetime',
            'updated_at' => 'datetime',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function cliente(): BelongsTo
    {
        return $this->belongsTo(Cliente::class);
    }

    public function detalles(): HasMany
    {
        return $this->hasMany(PedidoDetalle::class);
    }

    public function venta(): BelongsTo
    {
        return $this->belongsTo(Venta::class);
    }

    /**
     * @return array{id: int, numero: string, fecha: string, estado: string, total: float, metodo_pago: string|null, comprobante_pago: string|null, productos: array<int, array{producto_id: int|null, nombre: string, precio: float, cantidad: int, color: string|null, talla: string|null, imagen: string|null}>}
     */
    public function toClienteArray(): array
    {
        return [
            'id' => $this->id,
            'numero' => $this->numero,
            'fecha' => $this->created_at->toISOString(),
            'estado' => $this->estado,
            'total' => (float) $this->total,
            'tipo' => $this->tipo,
            'mesa' => $this->mesa,
            'observaciones' => $this->observaciones,
            'metodo_pago' => $this->metodo_pago,
            'comprobante_pago' => $this->comprobante_pago,
            'productos' => $this->detalles->map(fn (PedidoDetalle $detalle): array => [
                'producto_id' => $detalle->producto_id,
                'nombre' => $detalle->producto,
                'precio' => (float) $detalle->precio,
                'cantidad' => $detalle->cantidad,
                'color' => $detalle->color,
                'talla' => $detalle->talla,
                'imagen' => $detalle->imagen,
            ])->values()->all(),
        ];
    }
}
