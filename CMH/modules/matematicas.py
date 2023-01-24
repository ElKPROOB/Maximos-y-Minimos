import numpy as np

from modules.interfaz import *


def evaluar_matriz(matriz_hessiana: np.ndarray, dim: int, variables: list, puntos_a_usar: dict) -> np.ndarray:
    """
    Evalua la matriz Hessiana en todas sus variables.

    Parameters
    ----------
    matriz_hessiana : ndarray
        Matriz Hessiana a evaluar.
    dim : int
        Dimension de la función.
    variables : list
        Variables simbólicas de la función.
    puntos_a_usar : dict
        Valores asignados a cada variable.

    Returns
    -------
    ndarray
        Matriz de enteros.
    """
    for i in range(dim):
        for j in range(dim):
            if variables[0] in puntos_a_usar:
                matriz_hessiana[i][j] = matriz_hessiana[i][j].subs(
                    variables[0], puntos_a_usar[variables[0]]
                )
            if dim > 1 and variables[1] in puntos_a_usar:
                matriz_hessiana[i][j] = matriz_hessiana[i][j].subs(
                    variables[1], puntos_a_usar[variables[1]]
                )
            if dim > 2 and variables[2] in puntos_a_usar:
                matriz_hessiana[i][j] = matriz_hessiana[i][j].subs(
                    variables[2], puntos_a_usar[variables[2]]
                )
    escribir(txt="Matriz Hessiana Evaluada en el punto "+str(puntos_a_usar)
             .replace("{", "$(")
             .replace("}", r")$")
             .replace(", ", r",\hspace{2mm}")
             .replace("sqrt", r"\sqrt")
             .replace("log", "ln"),
             matriz=matriz_hessiana,
             dim=dim
             )
    return matriz_hessiana


def determinante(matriz: np.ndarray) -> object:
    """
    Devuelve el polinomio del determinante de una matriz.

    Parameters
    ----------
    matriz : ndarray
        Matriz (M - λi).

    Returns
    -------
    object
        Polinomio algebráico.
    """
    if matriz.shape == (1, 1):
        return matriz[0][0]
    eq = 0
    for i, elem in enumerate(matriz[0]):
        eq += (-1)**i*(
            elem *
            determinante(np.delete(
                np.delete(matriz, 0, 0),
                i, 1
            ))
        )
    return eq


def obtener_funcion(funcion_o: str) -> sym.Mul:
    """
    Obtiene la función simbólica a partir de un string.

    Parameters
    ----------
    funcion : str
        Función.

    Returns
    -------
    Mul
        Función simbólica.
    """
    funcion = sym.sympify(funcion_o)
    return funcion


def obtener_vector_gradiente(dim: int, vars: list, funcion: object) -> list:
    """
    Obtiene el vector gradiente de una función.

    Parameters
    ----------
    dim : int
        Dimensión de la función.
    vars : list
        Variables de la función.
    funcion : object
        Función simbólica.

    Returns
    -------
    list
        Vector gradiente.
    """
    vector_gradiente = []
    vector_gradiente.append(sym.diff(funcion, vars[0]))
    if dim > 1:
        vector_gradiente.append(sym.diff(funcion, vars[1]))
    if dim > 2:
        vector_gradiente.append(sym.diff(funcion, vars[2]))
    return vector_gradiente


def posibles_puntos(vector_gradiente: list, variables: list) -> list:
    """
    Obtiene los puntos donde el vector gradiente es igual al vector 0.

    Parameters
    ----------
    vector_gradiente : list
        Vector gradiente.
    variables : list
        Variables simbólicas de la función.

    Returns
    -------
    list
        Lista de posibles puntos (incluye imaginarios).
    """
    try:
        puntos = sym.solve(vector_gradiente, variables, dict=True)
    except NotImplementedError:
        print("No se pudo obtener los puntos críticos.")
        os.system("pause")
        return []
    return puntos


def obtener_matriz_hessiana(dim: int, vector_gradiente: list, variables: list) -> np.ndarray:
    """
    Obtiene la matriz Hessiana de una función.

    Parameters
    ----------
    dim : int
        Dimensión de la función.
    vector_gradiente : list
        Vector gradiente.
    variables : list
        Variables simbólicas de la función.

    Returns
    -------
    ndarray
        Matriz Hessiana.
    """
    matriz_hessiana = []
    for i in range(dim):
        renglon = []
        for j in range(dim):
            renglon.append(
                sym.diff(vector_gradiente[j], variables[i])
            )
        matriz_hessiana.append(renglon)
    matriz_hessiana = np.array(matriz_hessiana)
    return matriz_hessiana


def raices(matriz: np.ndarray, dim: int, variables: list, puntos_a_usar: dict) -> list:
    """
    Obtiene los valores de lambda (λ) en los que el determinante
    de la matriz Hessiana evaluada es igual a 0.

    Parameters
    ----------
    matriz : ndarray
        Matriz Hessiana.
    dim : int
        Dimensión de la función.
    variables : list
        Variables simbólicas de la función.
    puntos_a_usar : dict
        El punto a usar para evaluar la matriz Hessiana.

    Returns
    -------
    list
        Lista de posibles valores para λ.
    """
    matriz = evaluar_matriz(matriz, dim, variables, puntos_a_usar)
    lambda_ = sym.symbols('λ')
    matriz = matriz-(lambda_*np.identity(dim, dtype=int))
    escribir(matriz=matriz, dim=dim, tit=False)
    ecuacion = determinante(matriz)
    escribir(funcion=sym.Eq(ecuacion, 0))
    solucion = sym.solve(ecuacion, lambda_, list=True)
    escribir(txt="Los posibles valores para $\\lambda$ son: ",
             list_=list(solucion))
    return solucion


def normalizar_puntos(puntos: list, dim: int, variables: list) -> list:
    """
    Añade las variables que no se encuentren en los puntos y las ordena.

    Parameters
    ----------
    puntos : list
        Puntos a normalizar.
    dim : int
        Dimensión de la función.
    variables : list
        Variables simbólicas de la función.

    Returns
    -------
    list
        Puntos normalizados.
    """
    for elem in puntos:
        if not variables[0] in elem:
            elem[variables[0]] = variables[0]
        if dim > 1 and not variables[1] in elem:
            elem[variables[1]] = variables[1]
        if dim > 2 and not variables[2] in elem:
            elem[variables[2]] = variables[2]
    for elem in puntos:
        elem = dict(sorted(elem.items(), key=lambda x: str(x[0])))
    return puntos
