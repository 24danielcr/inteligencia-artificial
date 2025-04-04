import random
import time

class Estado:
    
    def __init__(self, columnas, movimientos=None):
        # Lista de columnas, cada columna es una lista de fichas (caracteres)
        self.columnas = columnas
        # Lista de movimientos realizados para llegar a este estado
        self.movimientos = movimientos if movimientos else []
    
    def copia(self):
        """Crea una copia del estado actual"""
        nuevas_columnas = [list(col) for col in self.columnas]
        nuevos_movimientos = list(self.movimientos)
        return Estado(nuevas_columnas, nuevos_movimientos)
    
    def es_solucion(self):
        """Verifica si el estado actual es una solución válida"""
        colores_agrupados = {}
        
        for columna in self.columnas:
            # Si la columna está vacía, continuar
            if not columna:
                continue
                
            # Obtener el color de la columna
            color = columna[0]
            
            # Verificar que todas las fichas en la columna sean del mismo color
            if not all(ficha == color for ficha in columna):
                return False
            
            # Verificar que no haya otro color agrupado en otra columna
            if color in colores_agrupados:
                return False
            
            # Añadir este color a los colores agrupados
            colores_agrupados[color] = True
            
            # Verificar que haya exactamente 4 fichas de ese color
            if len(columna) != 4:
                return False
        
        # Verificar que todos los colores estén agrupados
        return len(colores_agrupados) == 4
    
    def calcular_heuristica(self):
        """
        Calcula un valor heurístico que estima la distancia a la solución.
        Un valor menor indica un estado más cercano a la solución.
        """
        # Diccionario para contar cuántas fichas de cada color hay en cada columna
        conteo = {}
        
        # Colores disponibles
        colores = ['R', 'G', 'Y', 'B']
        
        # Para cada columna
        for i, columna in enumerate(self.columnas):
            for ficha in columna:
                if (i, ficha) not in conteo:
                    conteo[(i, ficha)] = 0
                conteo[(i, ficha)] += 1
        
        # Inicializamos el valor heurístico
        h = 0
        
        # Penalización por fichas mal colocadas
        for i, columna in enumerate(self.columnas):
            if not columna:
                continue
            
            # Contamos cuántos colores diferentes hay en la columna
            colores_en_columna = set(columna)
            
            # Si hay más de un color en la columna, hay que mover fichas
            if len(colores_en_columna) > 1:
                # Encontramos el color mayoritario
                color_mayoritario = max(colores_en_columna, key=lambda c: columna.count(c))
                # Penalizamos por cada ficha que no sea del color mayoritario
                h += sum(1 for ficha in columna if ficha != color_mayoritario)
            
            # Si hay menos de 4 fichas del mismo color, necesitamos traer más
            if len(columna) == 4 and len(colores_en_columna) == 1:
                # Esta columna ya está bien formada, no penalizar
                pass
            else:
                # Penalizar por la diferencia hasta completar 4 fichas del mismo color
                h += 1
        
        # Penalización por colores dispersos
        for color in colores:
            # Contar en cuántas columnas diferentes está presente este color
            columnas_con_color = set(i for (i, c), _ in conteo.items() if c == color)
            # Penalizar por dispersión (si está en más de una columna)
            h += len(columnas_con_color) - 1 if columnas_con_color else 0
        
        return h
    
    def generar_sucesores(self):
        """Genera todos los posibles estados sucesores a partir del estado actual"""
        sucesores = []
        
        # Para cada columna origen
        for i, columna_origen in enumerate(self.columnas):
            if not columna_origen:  # Si la columna está vacía, no hay ficha para mover
                continue
            
            # Ficha en la parte superior de la columna origen
            ficha = columna_origen[-1]
            
            # Para cada columna destino
            for j, columna_destino in enumerate(self.columnas):
                if i == j:  # No tiene sentido mover a la misma columna
                    continue
                
                # Verificar que la columna destino no supere el límite de 6 fichas
                if len(columna_destino) >= 6:
                    continue  # Salta esta columna y busca otra
                
                # Regla 1: Solo se puede mover a una columna vacía
                # Regla 2: Solo se puede mover a una columna cuya ficha superior sea del mismo color
                # Regla 3: Si la columna origen solo tiene una ficha de un color, no la movemos a una columna vacía
                if (not columna_destino) or (columna_destino and columna_destino[-1] == ficha):
                    # Evitar movimientos inútiles: no mover la única ficha a una columna vacía
                    if not columna_destino and len(columna_origen) == 1:
                        continue
                    
                    # Crear un nuevo estado moviendo la ficha
                    nuevo_estado = self.copia()
                    nuevo_estado.columnas[i] = nuevo_estado.columnas[i][:-1]  # Quitar la ficha de la columna origen
                    nuevo_estado.columnas[j] = nuevo_estado.columnas[j] + [ficha]  # Añadir la ficha a la columna destino
                    
                    # Registrar el movimiento
                    nuevo_movimiento = f"Mover {ficha} de columna {i+1} a columna {j+1}"
                    nuevo_estado.movimientos.append(nuevo_movimiento)
                    
                    sucesores.append(nuevo_estado)
        
        # Ordeno sucesores segun heuristica para encontrar más rapido la soluciuón
        sucesores.sort(key=lambda s: s.calcular_heuristica())

        return sucesores


def ids_con_heuristica(estado_inicial):
    """
    Implementa un algoritmo IDS con límite inicial basado en heurística
    - La profundidad máxima en cada iteración se basa en la heurística inicial
    - No almacena estados previos (exploración en caliente)
    """
    # Establecer el límite de profundidad inicial basado en la heurística
    limite_profundidad = estado_inicial.calcular_heuristica()
    print(f"Límite de profundidad inicial dado por la Heurística: {limite_profundidad}")
    
    # Establecemos un contador de nodos
    global nodos_visitados_global
    global heuristica

    for limite in range(1, limite_profundidad + 1):
      nodos_visitados_global = 0
      heuristica = limite_profundidad
      
      # Llamamos a la búsqueda en profundidad limitada por la heuristica
      solucion = busqueda_profundidad_limitada(estado_inicial, limite)
      
      # Si encontramos la solución, la devolvemos
      if solucion:
          print(f"¡Solución encontrada en la profundidad {len(solucion.movimientos)}!")
          return solucion

      # Si no se encuentra solución en esta iteración, incrementamos el límite de profundidad
      print(f"No se encontró solución en el límite {limite}. Nodos explorados: {nodos_visitados_global}")

    return None  # No se encontró solución



def busqueda_profundidad_limitada(estado, limite, profundidad=0):
    """
    Función recursiva para implementar la búsqueda en profundidad limitada
    """
    global nodos_visitados_global
    nodos_visitados_global += 1
    
    # Si el estado actual es la solución, retornamos los movimientos
    if estado.es_solucion():
        print(f"¡Solución encontrada! Nodos explorados: {nodos_visitados_global}")
        return estado
    
    # Si hemos alcanzado el límite de profundidad, retornamos None
    if profundidad >= limite:
        return None
    
    # Generamos los sucesores
    sucesores = estado.generar_sucesores()
    
    # Calcular la heurística para ver si voy en buen camino
    '''
    mejor_h = float('inf')
    for s in sucesores: # Obtenemos la mejor euristica de los sucesores
        h = s.calcular_heuristica()
        mejor_h = min(mejor_h, h)
    
    global heuristica
    if mejor_h < heuristica :
        heuristica = mejor_h
        print(f"Profundidad: {profundidad}, Mejor heutistica de sucesores: {mejor_h}, Nodos visitados: {nodos_visitados_global}")
    '''
    
    # Exploramos cada sucesor
    for sucesor in sucesores:
        # Llamada recursiva con incremento de profundidad estándar
        resultado = busqueda_profundidad_limitada(sucesor, limite, profundidad + 1)
        
        # Si encontramos una solución, la devolvemos
        if resultado:
            return resultado
    
    # Si no encontramos solución en este camino
    return None