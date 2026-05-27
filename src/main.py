import time
from loaders.cargador_wikipedia import CargadorWikipedia
from utilidades.reporte_basico import ReporteBasicoWikipedia


def main():
    inicio = time.perf_counter()

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

    puntajes = grafo.pagerank()

    ranking = list(puntajes.items())

    ranking.sort(key=lambda item: item[1], reverse=True)

    print("Top 10 según algoritmo Page Rank:")
    for id_articulo, puntaje in ranking[:10]:
        print(f"{id_articulo}: {puntaje}")

    fin = time.perf_counter()
    tiempo_total = fin - inicio
    print(f"\nTiempo total de ejecución: {round(tiempo_total, 4)} segundos")

if __name__ == "__main__":
    main()
