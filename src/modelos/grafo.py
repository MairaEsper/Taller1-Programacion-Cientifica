from collections import deque

from modelos.articulo import ArticuloWikipedia


class GrafoWikipedia:
    """Representa un grafo dirigido de articulos de Wikipedia y sus enlaces."""

    def __init__(self):
        self.articulos = {}
  
    def agregar_articulo(self, id_articulo, nombre):
        articulo = ArticuloWikipedia(id_articulo, nombre)
        self.articulos[id_articulo] = articulo

    def obtener_articulo(self, id_articulo):
        return self.articulos[id_articulo]
    
    def agregar_categoria(self, id_articulo, categoria):
        self.articulos[id_articulo].agregar_categoria(categoria)

    def agregar_enlace(self, id_origen, id_destino):
        self.articulos[id_origen].agregar_enlace_salida(id_destino)
        self.articulos[id_destino].agregar_enlace_entrada(id_origen)

    def cantidad_articulos(self):
        return len(self.articulos)

    def cantidad_enlaces(self):
        sum = 0
        for articulo in self.articulos.values():
            sum += articulo.grado_salida()
        return sum

    def top_por_grado_entrada(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda articulo: articulo.grado_entrada(), reverse=True)
        return lista[:cantidad]

    def top_por_grado_salida(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda articulo: articulo.grado_salida(), reverse=True)
        return lista[:cantidad]

    def resumen(self):
        return {
            "articulos": self.cantidad_articulos(),
            "enlaces": self.cantidad_enlaces(),
        }

    def bfs(self, id_inicio, id_objetivo):
        """
        TODO:
        Implementar recorrido BFS.

        Sugerencia:
        - usar una cola (`deque`);
        - marcar visitados;
        - retornar el orden de visita.
        """
        if id_inicio or id_objetivo not in self.articulos:
            return -1


        #id_inicio = 2
        #id_objetivo = 7

        visitados = set([id_inicio]) #[2, 4, 3, 0, 6, 7, 5, 1]
        cola = deque([(id_inicio, 0)]) # [(5, 2), (1, 2)]


        while cola:
            actual = cola.popleft() # (7, 2)
            id_actual = actual[0] #7
            cant_enlaces = actual[1] #2

            if id_actual == id_objetivo:
                return cant_enlaces
            

            for vecino in self.articulos[id_actual].enlaces_salida:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, cant_enlaces + 1))


        return -1

    def dfs(self, id_inicio):
        """
        TODO:
        Completar o reescribir este método usando una pila o recursión.
        """
        if id_inicio not in self.articulos:
            return []

        visitados = set() 
        pila = [id_inicio] 
        recorrido = [] 

        while pila:
            actual = pila.pop()

            if actual in visitados:
                continue

            visitados.add(actual)
            recorrido.append(actual)

            vecinos = list(self.articulos[actual].enlaces_salida) 
            vecinos.reverse() 

            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)

        return recorrido

    def encontrar_camino_simple(self, id_origen, id_destino):
        """
        TODO:
        Mejorar esta búsqueda para encontrar caminos más interesantes.
        Por ahora retorna un camino simple usando BFS.
        """
        if id_origen not in self.articulos or id_destino not in self.articulos:
            return []

        cola = deque([id_origen])
        padres = {id_origen: None}

        while cola:
            actual = cola.popleft()

            if actual == id_destino:
                break

            for vecino in self.articulos[actual].enlaces_salida:
                if vecino not in padres:
                    padres[vecino] = actual
                    cola.append(vecino)

        if id_destino not in padres:
            return []

        camino = []
        actual = id_destino

        while actual is not None:
            camino.append(actual)
            actual = padres[actual]

        camino.reverse()
        return camino

    def pagerank(self, iteraciones=20, damping=0.85):
        cantidad_nodos = self.cantidad_articulos()
        if cantidad_nodos == 0:
            return {}

        puntajes = {}
        valor_inicial = 1.0 / cantidad_nodos

        for id_articulo in self.articulos:
            puntajes[id_articulo] = valor_inicial

        for _ in range(iteraciones):
            nuevos_puntajes = {}

            for id_articulo in self.articulos:
                nuevos_puntajes[id_articulo] = (1.0 - damping) / cantidad_nodos

            for id_articulo, articulo in self.articulos.items():
                if articulo.grado_salida() == 0:
                    continue

                aporte = puntajes[id_articulo] / articulo.grado_salida()

                for vecino in articulo.enlaces_salida:
                    nuevos_puntajes[vecino] += damping * aporte

            puntajes = nuevos_puntajes

        return puntajes
