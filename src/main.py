from loaders.cargador_wikipedia import CargadorWikipedia
from utilidades.reporte_basico import ReporteBasicoWikipedia


def main():
    cargador = CargadorWikipedia()
    grafo = cargador.cargar_grafo()
    reporte = ReporteBasicoWikipedia()
    archivos_reporte = reporte.generar(grafo)
    reporte.imprimir_en_consola(grafo)

    print()
    print("Archivos generados:")
    print(archivos_reporte["texto"])

    print()
    print("Siguientes pasos sugeridos:")
    print("Completar analisis de BFS y DFS.")
    print("Implementar PageRank y exportar resultados.")
    
    menor_camino = grafo.bfs(2, 6354)
    print("Menor camino de 2 a 6354:", menor_camino)

    dfs = grafo.dfs(2,3)
    print("Hay ciclo en 2 y 3:", dfs)

if __name__ == "__main__":
    main()
