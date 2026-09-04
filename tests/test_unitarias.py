"""
PRUEBAS UNITARIAS (las escribes TU, el estudiante).

Aqui debes ir agregando tus propias pruebas unitarias, siguiendo el ciclo
TDD (rojo - verde - refactor), ANTES de escribir cada pequena porcion de
codigo en venta_entradas/modelos.py.

Ejemplo de como se ve una prueba unitaria (borrala y escribe las tuyas):

def test_ejemplo_evento_guarda_su_nombre():
    from venta_entradas.modelos import Evento
    evento = Evento("Teatro", aforo_maximo=10, precio_entrada=25.0)
    assert evento.nombre == "Teatro"

Recomendacion de orden sugerido (puedes seguir otro si prefieres):
1. Pruebas de la clase Evento (constructor, entradas_disponibles, etc).
2. Pruebas de SistemaVentas.registrar_evento.
3. Pruebas de SistemaVentas.vender_entradas (casos validos e invalidos).
4. Pruebas de SistemaVentas.calcular_total_con_descuento.

Para ejecutar solo tus pruebas unitarias:
    pytest tests/test_unitarias.py -v

Para ejecutar TODO (unitarias + aceptacion):
    pytest -v
"""

import pytest

from venta_entradas.modelos import Evento, SistemaVentas, VentaError


def crear_evento(nombre="Rojos vs. Cremas", aforo=100, precio=150.0):
    return Evento(nombre, aforo_maximo=aforo, precio_entrada=precio)


def test_evento_guarda_datos_e_inicia_sin_ventas():
    evento = crear_evento(aforo=50, precio=125.0)

    assert evento.nombre == "Rojos vs. Cremas"
    assert evento.aforo_maximo == 50
    assert evento.precio_entrada == 125.0
    assert evento.entradas_vendidas == 0


def test_entradas_disponibles_se_calculan_con_las_ventas():
    sistema = SistemaVentas()
    evento = crear_evento(aforo=10)
    sistema.registrar_evento(evento)

    sistema.vender_entradas(evento.nombre, 3)

    assert evento.entradas_disponibles == 7


def test_hay_disponibilidad_respeta_el_aforo_restante():
    evento = crear_evento(aforo=4)

    assert evento.hay_disponibilidad(4) is True
    assert evento.hay_disponibilidad(5) is False
    assert evento.hay_disponibilidad(0) is False


def test_registrar_evento():
    sistema = SistemaVentas()
    evento = crear_evento()

    sistema.registrar_evento(evento)

    assert sistema.eventos[evento.nombre] is evento


def test_registrar_evento_repetido_lanza_error():
    sistema = SistemaVentas()
    evento = crear_evento()
    sistema.registrar_evento(evento)

    with pytest.raises(VentaError):
        sistema.registrar_evento(evento)


def test_vender_entradas_exito():
    sistema = SistemaVentas()
    evento = crear_evento(precio=200.0)
    sistema.registrar_evento(evento)

    total = sistema.vender_entradas(evento.nombre, 2)

    assert total == 400.0
    assert evento.entradas_vendidas == 2


def test_vender_mas_entradas_de_las_disponibles():
    sistema = SistemaVentas()
    evento = crear_evento(aforo=2)
    sistema.registrar_evento(evento)

    with pytest.raises(VentaError):
        sistema.vender_entradas(evento.nombre, 3)

    assert evento.entradas_vendidas == 0


@pytest.mark.parametrize("cantidad", [0, -1])
def test_vender_cero_o_menos_entradas(cantidad):
    sistema = SistemaVentas()
    evento = crear_evento()
    sistema.registrar_evento(evento)

    with pytest.raises(VentaError):
        sistema.vender_entradas(evento.nombre, cantidad)


def test_vender_para_evento_inexistente_lanza_error():
    sistema = SistemaVentas()

    with pytest.raises(VentaError):
        sistema.vender_entradas("Evento Fantasma", 1)


def test_descuento_por_cantidad_no_registra_venta():
    sistema = SistemaVentas()
    evento = crear_evento(precio=100.0)
    sistema.registrar_evento(evento)

    total = sistema.calcular_total_con_descuento(
        evento.nombre, cantidad=3, porcentaje_descuento=20
    )

    assert total == 240.0
    assert evento.entradas_vendidas == 0


@pytest.mark.parametrize("descuento", [-1, 101])
def test_descuento_invalido(descuento):
    sistema = SistemaVentas()
    evento = crear_evento()
    sistema.registrar_evento(evento)

    with pytest.raises(VentaError):
        sistema.calcular_total_con_descuento(
            evento.nombre, cantidad=1, porcentaje_descuento=descuento
        )


def test_estado_de_ventas_se_conserva_entre_compras():
    sistema = SistemaVentas()
    evento = crear_evento(aforo=10)
    sistema.registrar_evento(evento)

    sistema.vender_entradas(evento.nombre, 2)
    sistema.vender_entradas(evento.nombre, 3)

    assert evento.entradas_vendidas == 5
    assert evento.entradas_disponibles == 5
