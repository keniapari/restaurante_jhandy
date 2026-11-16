<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('pedidos', function (Blueprint $table) {
            $table->foreignId('cliente_id')->nullable()->after('user_id')->constrained('clientes')->nullOnDelete();
            $table->string('tipo', 20)->default('online')->after('estado');
            $table->string('mesa', 20)->nullable()->after('tipo');
            $table->text('observaciones')->nullable()->after('mesa');
        });

        Schema::table('pedido_detalles', function (Blueprint $table) {
            $table->foreignId('plato_id')->nullable()->after('producto_id')->constrained('platos')->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::table('pedido_detalles', function (Blueprint $table) {
            $table->dropConstrainedForeignId('plato_id');
        });

        Schema::table('pedidos', function (Blueprint $table) {
            $table->dropConstrainedForeignId('cliente_id');
            $table->dropColumn(['tipo', 'mesa', 'observaciones']);
        });
    }
};
