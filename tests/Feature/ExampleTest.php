<?php

test('las imagenes del restaurante existen', function () {
    expect(public_path('images/restaurant/interior.jpg'))->toBeFile();
    expect(public_path('images/restaurant/plato-1.jpg'))->toBeFile();
    expect(public_path('images/restaurant/plato-2.jpg'))->toBeFile();
    expect(public_path('images/restaurant/logo.svg'))->toBeFile();
});

test('la ruta principal muestra el menu para invitados', function () {
    $this->get(route('principal'))->assertOk();
});
