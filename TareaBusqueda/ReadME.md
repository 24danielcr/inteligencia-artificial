# Proyecto de Resolución de Problemas de Agrupación de Fichas


## Requisitos previos

- Python 3.7 o superior.

## Ejecución de la tarea

3. Ejecute el archivo `main.py` para comenzar a interactuar con el programa.

## Descripción de la tarea

El programa simula un tablero con 6 columnas y hasta 6 fichas por columna. El objetivo es organizar las fichas, que pueden ser de 4 colores distintos, en un estado que cumpla con ciertas condiciones de validez para cada columna. El programa permite probar diferentes algoritmos de búsqueda para resolver este problema, tanto con heurística como sin ella.

## Interacción con el Programa

Una vez que ejecute el programa, verá un menú interactivo que pedirá elegir una de las siguientes opciones:

1. **Búsqueda sin Heurística**: Utiliza la búsqueda sin heurística para encontrar la solución.

2. **Búsqueda A\***: Utiliza la búsqueda A\* con una heurística definida para encontrar la solución.

3. **Búsqueda IDS**: Utiliza la búsqueda IDS con límite de nodos explorados.

4. **Todas Juntas**: Ejecuta todas las búsquedas y muestra los resultados.

## Estructura de Archivos

### Archivos principales

- **main.py**: Es el archivo principal que gestiona la interacción con el usuario, genera los estados iniciales aleatorios y ejecuta los algoritmos de búsqueda.
- **noHeuristica.py**: Contiene la implementación de la búsqueda sin heurística.
- **IDS.py**: Contiene la implementación de la búsqueda IDS con heurística.

## Métodos de Búsqueda

### Búsqueda sin Heurística

Este método de búsqueda no utiliza ninguna heurística, simplemente explora los estados de manera iterativa hasta encontrar la solución. 

### Búsqueda A\*

A\* es un algoritmo de búsqueda informado que utiliza una heurística para guiar la búsqueda de manera eficiente hacia la solución. Se basa en una función de coste que combina el coste desde el estado inicial hasta el estado actual y una estimación del coste restante hasta la solución.

### Búsqueda IDS (Iterative Deepening Search)

Este algoritmo realiza una búsqueda por profundidad limitada, aumentando progresivamente el límite de profundidad. Es eficiente en cuanto a memoria y puede encontrar soluciones a problemas de búsqueda profunda. En este caso, se utiliza con una heurística para guiar la exploración.

## Estudiantes

- C08538 - Christopher Víquez
- C10577 - Sebastián Arce
- C23310 - Daniel Gómez
- C07901 - Francisco Ulate
