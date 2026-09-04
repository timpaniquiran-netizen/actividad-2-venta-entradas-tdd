# Venta de Entradas - MVP con TDD

Repositorio público: https://github.com/timpaniquiran-netizen/actividad-2-venta-entradas-tdd

Actividad 2 de Ingeniería del Software Avanzada. El proyecto implementa el
código de partida proporcionado por la docente y conserva sin cambios las siete
pruebas de aceptación oficiales.

Como complemento se incluye el prototipo E-Tickets del Clásico Nacional entre
Municipal y Comunicaciones, ejecutable desde Jupyter en Anaconda.

## Requisitos

- Python 3.9 o superior
- pytest
- Jupyter Notebook o JupyterLab para abrir el prototipo visual

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Ejecutar las pruebas

Solo las pruebas de aceptación oficiales:

```bash
python -m pytest tests/test_aceptacion.py -v
```

Todas las pruebas:

```bash
python -m pytest -v
```

El resultado final esperado es `21 passed`: 7 pruebas de aceptación y 14 casos
unitarios propios.

## Ejecutar el prototipo visual

1. Abrir `E_Tickets_Rojos_vs_Cremas.ipynb` desde Jupyter en Anaconda.
2. Ejecutar la celda principal de la aplicación.
3. Abrir `http://127.0.0.1:8765` en el navegador.
4. Ejecutar la celda de pytest para comprobar las pruebas oficiales y propias.
5. Al terminar, ejecutar la última celda para detener la aplicación.

## Estructura

```text
venta_entradas/modelos.py       Implementación de Evento y SistemaVentas
tests/test_aceptacion.py        Pruebas oficiales sin modificar
tests/test_unitarias.py         Pruebas unitarias desarrolladas con TDD
evidencias/                     Resultados de las fases roja y verde
E_Tickets_Rojos_vs_Cremas.ipynb Prototipo visual para Jupyter
```
