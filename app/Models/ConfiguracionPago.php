<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['qr_pago'])]
/**
 * @property string|null $qr_pago
 */
class ConfiguracionPago extends Model
{
    public static function actual(): self
    {
        return static::query()->firstOrCreate([]);
    }
}
