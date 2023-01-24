from modules.matematicas import *


def main():
    funcion = input("Ingrese la funcion: ")
    try:
        funcion = obtener_funcion(funcion)
    except:
        print("Entrada no válida")
        return
    variables = list(funcion.free_symbols)
    variables = sorted(variables, key=lambda k: str(k))
    dim = len(variables)
    if dim > 3 or dim < 1:
        print("Funcion de dimensión invalida")
        return
    vector_gradiente = obtener_vector_gradiente(dim, variables, funcion)
    escribir(0, txt=str(funcion), funcion=funcion)
    escribir(1, txt="Puntos singulares:")
    escribir(2, txt="La función es diferenciable en su dominio")
    escribir(1, txt="La función no tiene puntos frontera")
    escribir(1, txt="Puntos estacionarios:")
    escribir(txt="Vector Gradiente", vector=vector_gradiente, dim=dim)
    puntos = posibles_puntos(vector_gradiente, variables)
    puntos = normalizar_puntos(puntos, dim, variables)
    escribir(3, txt="Puntos en los que el vector gradiente es 0:")
    for i in puntos:
        escribir(5, txt=str(i))
    matriz_hessiana = obtener_matriz_hessiana(dim, vector_gradiente, variables)
    escribir(txt="Matriz Hessiana", matriz=matriz_hessiana, dim=dim)
    cont = 0
    for i in puntos:
        if all(j.is_real for j in i.values()):
            cont += 1
            matriz_hessiana_c = matriz_hessiana.copy()
            solucion = raices(
                matriz_hessiana_c, dim, variables, i
            )
            if all(j > 0 for j in solucion):
                solucion = "Mínimo Relativo"
            elif all(j < 0 for j in solucion):
                solucion = "Máximo Relativo"
            else:
                solucion = "Punto Silla"
            print(f"    -> {i}: {solucion}\n")
            resultados = f"Se tiene un ul({solucion})ul en el punto {i}"
            escribir(4, txt=resultados)
    if cont == 0:
        print("No hay puntos estacionarios")
        escribir(3, txt="No hay puntos estacionarios")
    escribir_tex(r"\end{document}", "a")


if __name__ == "__main__":
    main()
