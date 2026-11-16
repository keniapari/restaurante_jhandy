<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class UsuariosSeeder extends Seeder
{
    public function run(): void
    {
        $users = [
            ['name' => 'Propietaria', 'email' => 'admin@gmail.com', 'password' => 'admin1234', 'role' => 'admin'],
            ['name' => 'Cajera', 'email' => 'vendedora@gmail.com', 'password' => 'vendedora1234', 'role' => 'vendedor'],
            ['name' => 'Cocinera', 'email' => 'inventario@gmail.com', 'password' => 'inventario1234', 'role' => 'encargado_inventario'],
        ];

        foreach ($users as $data) {
            $user = User::updateOrCreate(
                ['email' => $data['email']],
                [
                    'name' => $data['name'],
                    'password' => bcrypt($data['password']),
                    'email_verified_at' => now(),
                    'role' => $data['role'],
                ]
            );

            $user->assignRole($data['role']);
        }
    }
}
