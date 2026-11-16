<?php

use App\Enums\Permission as PermissionEnum;
use App\Models\Permission;
use App\Models\Role;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    public function up(): void
    {
        foreach (PermissionEnum::cases() as $permiso) {
            Permission::updateOrCreate(
                ['nombre' => $permiso->value],
                [
                    'descripcion' => $permiso->label(),
                    'grupo' => $permiso->group(),
                ]
            );
        }

        $defaults = [
            Role::ADMIN => PermissionEnum::valuesForAdministrador(),
            Role::VENDEDOR => PermissionEnum::valuesForVendedor(),
            Role::ENCARGADO_INVENTARIO => PermissionEnum::valuesForEncargadoInventario(),
        ];

        foreach ($defaults as $roleName => $permissions) {
            Role::where('nombre', $roleName)->first()?->syncPermissionsByName($permissions);
        }
    }

    public function down(): void
    {
        $names = [
            PermissionEnum::MenuVer->value,
            PermissionEnum::PlatosVer->value,
            PermissionEnum::PlatosGestion->value,
            PermissionEnum::ReservasVer->value,
            PermissionEnum::ReservasGestion->value,
        ];

        Permission::whereIn('nombre', $names)->get()->each(function (Permission $permission): void {
            $permission->roles()->detach();
            $permission->delete();
        });
    }
};
