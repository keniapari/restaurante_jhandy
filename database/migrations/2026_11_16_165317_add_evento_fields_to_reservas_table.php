<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('reservas', function (Blueprint $table) {
            $table->string('tipo_evento', 30)->default('reunion')->after('personas');
            $table->unsignedSmallInteger('cantidad_platos')->default(11)->after('tipo_evento');
            $table->string('metodo_pago', 20)->default('efectivo')->after('cantidad_platos');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('reservas', function (Blueprint $table) {
            $table->dropColumn(['tipo_evento', 'cantidad_platos', 'metodo_pago']);
        });
    }
};
