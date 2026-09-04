"""
PRUEBAS DE ACEPTACION (proporcionadas por el profesor).

NO MODIFICAR este archivo.

Estas pruebas describen, desde el punto de vista del usuario final, el
comportamiento que debe tener el sistema de venta de entradas cuando este
completo. Mientras el codigo en venta_entradas/modelos.py no este
implementado, todas estas pruebas fallaran (fase ROJA). Tu objetivo es
implementar el codigo (usando TDD, con tus propias pruebas unitarias en
tests/test_unitarias.py) hasta que todas estas pruebas pasen (fase VERDE).

Para ejecutarlas:
    pytest tests/test_aceptacion.py -v
"""
import pytest

from venta_entradas.modelos import Evento, SistemaVentas, VentaError


def crear_sistema_con_evento(aforo=100, precio=50.0):
    sistema = SistemaVentas()
    evento = Evento("Concierto Rock", aforo_maximo=aforo, precio_entrada=precio)
    sistema.registrar_evento(evento)
    return sistema, evento


def test_aceptacion_crear_evento_inicia_sin_entradas_vendidas():
    """Un evento recien creado no tiene entradas vendidas."""
    evento = Evento("Concierto Rock", aforo_maximo=100, precio_entrada=50.0)

    assert evento.entradas_vendidas == 0
    assert evento.entradas_disponibles == 100


def test_aceptacion_vender_entradas_dentro_del_aforo():
    """El usuario puede comprar entradas si hay aforo disponible."""
    sistema, evento = crear_sistema_con_evento(aforo=100, precio=50.0)

    total = sistema.vender_entradas("Concierto Rock", 3)

    assert total == 150.0
    assert evento.entradas_vendidas == 3
    assert evento.entradas_disponibles == 97


def test_aceptacion_no_se_puede_vender_mas_entradas_que_el_aforo():
    """El sistema debe rechazar una venta que exceda el aforo disponible."""
    sistema, evento = crear_sistema_con_evento(aforo=5, precio=20.0)

    sistema.vender_entradas("Concierto Rock", 5)

    with pytest.raises(VentaError):
        sistema.vender_entradas("Concierto Rock", 1)


def test_aceptacion_no_se_puede_vender_a_un_evento_inexistente():
    """El sistema debe rechazar una venta de un evento no registrado."""
    sistema = SistemaVentas()

    with pytest.raises(VentaError):
        sistema.vender_entradas("Evento Fantasma", 1)


def test_aceptacion_no_se_puede_vender_cantidad_invalida():
    """El sistema debe rechazar ventas de 0 o menos entradas."""
    sistema, _ = crear_sistema_con_evento()

    with pytest.raises(VentaError):
        sistema.vender_entradas("Concierto Rock", 0)


def test_aceptacion_calculo_de_total_con_descuento():
    """El usuario puede consultar el total con descuento antes de comprar."""
    sistema, _ = crear_sistema_con_evento(aforo=100, precio=100.0)

    total = sistema.calcular_total_con_descuento(
        "Concierto Rock", cantidad=2, porcentaje_descuento=10
    )

    assert total == 180.0


def test_aceptacion_descuento_invalido_lanza_error():
    """Un porcentaje de descuento fuera de 0-100 debe rechazarse."""
    sistema, _ = crear_sistema_con_evento()

    with pytest.raises(VentaError):
        sistema.calcular_total_con_descuento(
            "Concierto Rock", cantidad=1, porcentaje_descuento=150
        )
