"""
Logica de un sistema simple de venta de entradas para eventos.

Este archivo contiene la ESTRUCTURA del codigo (clases y metodos) SIN
implementar. Cada metodo lanza NotImplementedError.

Tu tarea (usando TDD):
1. Ejecuta las pruebas de aceptacion (tests/test_aceptacion.py) y comprueba
   que fallan (fase ROJA).
2. Elige una funcionalidad pequena.
3. Escribe una prueba unitaria propia en tests/test_unitarias.py para esa
   funcionalidad (ROJO).
4. Implementa el codigo minimo aqui para que esa prueba pase (VERDE).
5. Mejora el codigo si hace falta sin romper las pruebas (REFACTOR).
6. Repite hasta que TODAS las pruebas (unitarias y de aceptacion) pasen.

No debes cambiar los nombres de las clases ni de los metodos, porque las
pruebas de aceptacion ya dependen de ellos. Si necesitas metodos o clases
auxiliares adicionales, puedes agregarlos libremente.
"""


class Evento:
    """Representa un evento con un aforo (cupo maximo de entradas)."""

    def __init__(self, nombre: str, aforo_maximo: int, precio_entrada: float):
        """
        Guarda el nombre del evento, el aforo maximo permitido y el precio
        de cada entrada. Debe inicializar tambien un contador de entradas
        vendidas en 0.
        """
        self.nombre = nombre
        self.aforo_maximo = aforo_maximo
        self.precio_entrada = precio_entrada
        self._entradas_vendidas = 0

    @property
    def entradas_vendidas(self) -> int:
        """Devuelve cuantas entradas se han vendido hasta el momento."""
        return self._entradas_vendidas

    @property
    def entradas_disponibles(self) -> int:
        """Devuelve cuantas entradas quedan disponibles (aforo - vendidas)."""
        return self.aforo_maximo - self._entradas_vendidas

    def hay_disponibilidad(self, cantidad: int) -> bool:
        """Devuelve True si se pueden vender 'cantidad' entradas mas."""
        return cantidad > 0 and cantidad <= self.entradas_disponibles


class VentaError(Exception):
    """Excepcion que se lanza cuando una venta no se puede realizar."""
    pass


class SistemaVentas:
    """Gestiona la venta de entradas para uno o varios eventos."""

    def __init__(self):
        """Inicializa la estructura donde se guardaran los eventos."""
        self.eventos = {}

    def registrar_evento(self, evento: Evento) -> None:
        """Agrega un evento nuevo al sistema."""
        if evento.nombre in self.eventos:
            raise VentaError("El evento ya se encuentra registrado.")
        self.eventos[evento.nombre] = evento

    def vender_entradas(self, nombre_evento: str, cantidad: int) -> float:
        """
        Vende 'cantidad' entradas del evento indicado.

        Reglas de negocio:
        - Si el evento no existe, debe lanzar VentaError.
        - Si 'cantidad' es menor o igual a 0, debe lanzar VentaError.
        - Si no hay aforo disponible para esa cantidad, debe lanzar
          VentaError.
        - Si la venta es valida, debe aumentar las entradas vendidas del
          evento y devolver el monto total a cobrar (cantidad * precio).
        """
        evento = self._buscar_evento(nombre_evento)
        self._validar_cantidad(cantidad)
        if not evento.hay_disponibilidad(cantidad):
            raise VentaError("No hay suficientes entradas disponibles.")

        evento._entradas_vendidas += cantidad
        return cantidad * evento.precio_entrada

    def calcular_total_con_descuento(
        self, nombre_evento: str, cantidad: int, porcentaje_descuento: float
    ) -> float:
        """
        Calcula el total a cobrar por 'cantidad' entradas del evento
        indicado, aplicando un porcentaje de descuento (0 a 100).

        Reglas de negocio:
        - No debe registrar la venta, solo calcular el monto.
        - Si el porcentaje esta fuera del rango 0-100, debe lanzar
          VentaError.
        - El resultado es: cantidad * precio_entrada * (1 - descuento/100)
        """
        evento = self._buscar_evento(nombre_evento)
        self._validar_cantidad(cantidad)
        if not 0 <= porcentaje_descuento <= 100:
            raise VentaError("El descuento debe estar entre 0 y 100.")
        if not evento.hay_disponibilidad(cantidad):
            raise VentaError("No hay suficientes entradas disponibles.")

        subtotal = cantidad * evento.precio_entrada
        return subtotal * (1 - porcentaje_descuento / 100)

    def _buscar_evento(self, nombre_evento: str) -> Evento:
        try:
            return self.eventos[nombre_evento]
        except KeyError as error:
            raise VentaError("El evento no está registrado.") from error

    @staticmethod
    def _validar_cantidad(cantidad: int) -> None:
        if cantidad <= 0:
            raise VentaError("La cantidad debe ser mayor que cero.")
