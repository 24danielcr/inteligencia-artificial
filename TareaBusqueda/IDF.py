import random

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
        # Contamos fichas mal colocadas y grupos incompletos
        h = 0
        
        # Diccionario para contar cuántas fichas de cada color hay en cada columna
        conteo = {}
        
        # Para cada columna
        for i, columna in enumerate(self.columnas):
            if not columna:
                continue
            
            # Contamos cuántas fichas de cada color hay en esta columna
            for ficha in columna:
                if (i, ficha) not in conteo:
                    conteo[(i, ficha)] = 0
                conteo[(i, ficha)] += 1
        
        """Conteo heuristico para dar un limite de profundidad"""
        # Evaluamos cuántas fichas están mal colocadas
        for (col, color), cantidad in conteo.items():
            # Si hay menos de 4 fichas de este color en esta columna,
            # significa que o bien hay que mover estas fichas a otra columna,
            # o bien hay que traer más fichas a esta columna
            if cantidad < 4:
                # Calculamos cuántas fichas debemos mover (como mínimo)
                h += 4 - cantidad
            
            # Si hay fichas de diferentes colores en la misma columna
            otras_fichas = sum(conteo.get((col, c), 0) for c in ['R', 'G', 'Y', 'B'] if c != color)
            if otras_fichas > 0:
                h += otras_fichas
        
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
                
                # Verificar si se puede colocar la ficha en la columna destino
                if not columna_destino or columna_destino[-1] == ficha:
                    # Crear un nuevo estado moviendo la ficha
                    nuevo_estado = self.copia()
                    nuevo_estado.columnas[i] = nuevo_estado.columnas[i][:-1]  # Quitar la ficha de la columna origen
                    nuevo_estado.columnas[j] = nuevo_estado.columnas[j] + [ficha]  # Añadir la ficha a la columna destino
                    
                    # Registrar el movimiento
                    nuevo_movimiento = f"Mover {ficha} de columna {i+1} a columna {j+1}"
                    nuevo_estado.movimientos.append(nuevo_movimiento)
                    
                    sucesores.append(nuevo_estado)
        
        # Ordenamos los sucesores por su valor heurístico (de menor a mayor)
        sucesores.sort(key=lambda estado: estado.calcular_heuristica())
        
        return sucesores

def idf_star(estado_inicial):
    """
    Implementa el algoritmo IDF* (Iterative Deepening F*)
    - Búsqueda en profundidad iterativa con límite de profundidad basado en heurística
    - No almacena estados previos (exploración en caliente)
    """
    # Límite de profundidad inicial basado en la heurística
    limite_profundidad = estado_inicial.calcular_heuristica()
    
    print(f"Límite de profundidad: {limite_profundidad}")
    
    # Llamamos a la búsqueda en profundidad limitada
    solucion = busqueda_profundidad_limitada(estado_inicial, limite_profundidad, )
    
    # Si encontramos una solución, la devolvemos
    if solucion:
        return solucion
    
    # Si no encontramos solución después de max_iteraciones
    return None

def busqueda_profundidad_limitada(estado, limite, profundidad=1):
    """
    Función recursiva para implementar la búsqueda en profundidad limitada
    """
    # Si hemos alcanzado el límite de profundidad, retornamos None
    if profundidad > limite:
        return None
    
    # Si el estado actual es la solución, retornamos los movimientos
    if estado.es_solucion():
        return estado
    
    # Generamos los sucesores (ya ordenados por heurística)
    sucesores = estado.generar_sucesores()
    
    # Exploramos cada sucesor en orden de mejor heurística
    for sucesor in sucesores:
        # La función f(n) en A* es g(n) + h(n)
        # Aquí, g(n) es la profundidad actual y h(n) es la heurística
        f_sucesor = profundidad + sucesor.calcular_heuristica()
        
        # Solo exploramos si f(n) <= límite
        if f_sucesor <= limite:
            # Llamada recursiva
          resultado = busqueda_profundidad_limitada(sucesor, limite, profundidad + 1)
          
          # Si encontramos una solución, la devolvemos
          if resultado:
              return resultado
    
    # Si no encontramos solución en este camino
    return None

def crear_estado_inicial():
    """
    Crea un estado inicial aleatorio con 4 columnas ocupadas y 2 vacías,
    distribuyendo 4 fichas de cada color (R, G, Y, B) de manera aleatoria.
    """
    # Creamos la lista de todas las fichas disponibles
    fichas_disponibles = ['R', 'R', 'R', 'R',  # 4 fichas rojas
                         'G', 'G', 'G', 'G',   # 4 fichas verdes
                         'Y', 'Y', 'Y', 'Y',   # 4 fichas amarillas
                         'B', 'B', 'B', 'B']   # 4 fichas azules
    
    # Mezclamos las fichas
    random.shuffle(fichas_disponibles)
    
    # Seleccionamos 4 columnas al azar para ser ocupadas (de las 6 disponibles)
    columnas_ocupadas = random.sample(range(6), 4)
    
    # Inicializamos las 6 columnas vacías
    columnas = [[] for _ in range(6)]
    
    # Distribuimos las fichas aleatoriamente entre las columnas seleccionadas
    for ficha in fichas_disponibles:
        # Elegimos aleatoriamente una de las 4 columnas ocupadas
        columna_idx = random.choice(columnas_ocupadas)
        columnas[columna_idx].append(ficha)
    
    return Estado(columnas)

def imprimir_estado(estado):
    """Imprime el estado actual del tablero"""
    # Encontrar la altura máxima
    max_altura = len(estado.columnas)
    
    # Imprimir el tablero de arriba hacia abajo
    for i in range(max_altura-1, -1, -1):
        fila = ""

        for col in estado.columnas:
            if i < len(col):
                fila += f" {col[i]} "
            else:
                fila += " . "
        print(fila)
    
    # Imprimir los números de columna
    print(" 1  2  3  4  5  6 ")

# Ejemplo de uso
if __name__ == "__main__":
    print("Problema de ordenamiento de colores - IDF*")
    print()

    for n in range(1,11):
      estado_inicial = crear_estado_inicial()
      print(f"{n}. Estado inicial:")
      imprimir_estado(estado_inicial)
      
      solucion = idf_star(estado_inicial)
      
      if solucion:
          print()
          print(f"¡Solución encontrada en {len(solucion.movimientos)} movimientos!")
          #for i, mov in enumerate(solucion):
          #    print(f"Paso {i+1}: {mov}")
          #imprimir_estado(solucion)
      else:
          print("No se encontró solución.")

      print()