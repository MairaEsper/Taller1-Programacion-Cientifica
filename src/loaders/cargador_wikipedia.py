from pathlib import Path

from modelos.grafo import GrafoWikipedia


class CargadorWikipedia:
    """Carga desde el dataset los datos necesarios para construir el grafo."""

    def __init__(self, ruta_dataset=None):
        if ruta_dataset is None:
            self.ruta_dataset = Path(__file__).resolve().parent.parent.parent / "dataset"
        else:
            self.ruta_dataset = Path(ruta_dataset)

    def cargar_nombres_articulos(self):
        ruta = self.ruta_dataset / "wiki-topcats_pagenames.txt"
        nombres = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                nombres[indice] = linea.strip()

        return nombres

    def cargar_nombres_categorias(self):
        ruta = self.ruta_dataset / "wiki-topcats_Category_names.txt"
        categorias = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                categorias[indice] = linea.strip()

        return categorias

    def _leer_matriz_market(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:
                    fila = int(partes[0])
                    columna = int(partes[1])
                    yield fila, columna

    def cargar_grafo(self):
        grafo = GrafoWikipedia()
        
        nombres_articulos = self.cargar_nombres_articulos()
        for id, nombre in nombres_articulos.items():
            grafo.agregar_articulo(id,nombre)
            
        nombres_categorias = self.cargar_nombres_categorias()
        ruta_topcats_categories = self.ruta_dataset / "wiki-topcats_Categories.mtx"
        leer_matriz_categories = self._leer_matriz_market(ruta_topcats_categories)
        
        for fila, columna in leer_matriz_categories:
            grafo.agregar_categoria(fila, nombres_categorias[columna])
                    
        ruta_topcats = self.ruta_dataset / "wiki-topcats.mtx"
        leer_matriz_enlaces = self._leer_matriz_market(ruta_topcats)
        for fila, columna in leer_matriz_enlaces:
            grafo.agregar_enlace(fila, columna)
        
        return grafo
