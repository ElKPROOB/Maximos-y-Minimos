import os
from pathlib import Path

import sympy as sym


inicio_doc = r"""\documentclass[]{article}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}

\begin{document}"""


def escribir_tex(txt, m):
    """Función para escribir en un archivo .tex."""
    ruta = os.path.dirname(os.path.abspath(__file__))
    ruta = str(Path(ruta).parent)
    with open(ruta+r"\Files\Procedimiento.tex", m, encoding="utf-8") as f:
        f.write(txt)


def escribir(lvl=-1, txt="", funcion=None, matriz=None, vector=None, list_=[], dim=0, tit=True):
    """Función para clasificar el tipo de texto a escribir en el archivo .tex."""
    if lvl != -1:
        if lvl == 0:
            global inicio_doc
            escribir_tex(inicio_doc, "w")
            escribir_tex(r"{\large Función: }", "a")
            escribir_tex("$"+sym.latex(funcion)+"$\\\\\n\n", "a")
        elif lvl == 1:
            escribir_tex("\\noindent\n- "+txt+"\\\\\n\n", "a")
        elif lvl == 2:
            escribir_tex("\\noindent\n" +
                         r"\hspace{1cm}$\Rightarrow$ " +
                         txt + "\\\\\n\n", "a")
        elif lvl == 3:
            escribir_tex("\\noindent\n" +
                         r"\hspace{1cm}$\rightarrow$ " +
                         txt + "\\\\\n\n", "a")
        elif lvl == 4:
            escribir_tex(
                r"\textbf{\hspace{1cm}$\therefore$ " +
                (txt
                 .replace("{", "$(")
                 .replace("}", r")$")
                 .replace(", ", r",\hspace{2mm}")
                 .replace("ul(", r"\underline{")
                 .replace(")ul", r"}")
                 .replace("sqrt", r"\sqrt")
                 .replace("log", "ln")) +
                "\\\\}\n\n", "a")
        elif lvl == 5:
            escribir_tex(
                r"\textbf{\hspace{1cm}$\bullet$ " +
                (txt
                 .replace("{", "$(")
                 .replace("}", r")$")
                 .replace(", ", r",\hspace{2mm}")
                 .replace("ul(", r"\underline{")
                 .replace(")ul", r"}")
                 .replace("sqrt", r"\sqrt")
                 .replace("log", "ln")) +
                "\\\\}\n\n", "a")
    elif vector is not None:
        escribir_tex(
            "\\[\n\\text{\\textit{"+txt+": }}\n\\]\n\\[\n",
            "a")
        escribir_tex("\\left(\n\\begin{array}{ccc}\n", "a")
        for i in range(dim-1):
            escribir_tex(sym.latex(vector[i]).replace(r"\log", r"\ln") +
                         ", &\n", "a")
        escribir_tex(sym.latex(vector[dim-1]).replace(r"\log", r"\ln") +
                     "\n\\end{array}\n\\right)\n\\]\\\\\n\n", "a")
    elif matriz is not None:
        if tit:
            escribir_tex(
                "\\[\n\\text{\\textit{"+txt+": }}\n\\]\n\\[\n",
                "a")
        else:
            escribir_tex("\\[\n\\Rightarrow", "a")
        matriz_c = []
        for i in range(len(matriz)):
            matriz_c.append(list(matriz[i]))
        escribir_tex("\\left(\n\\begin{array}{ccc}\n", "a")
        for i in range(dim):
            for j in range(dim-1):
                escribir_tex(sym.latex(matriz[i][j])
                             .replace("λ", r"\lambda")
                             .replace(r"\log", r"\ln")
                             + " & ", "a")
            escribir_tex(sym.latex(matriz[i][dim-1])
                         .replace("λ", r"\lambda")
                         .replace(r"\log", r"\ln")
                         + "\\\\\n", "a")
        escribir_tex("\\end{array}\n\\right)\n\\]\\\\\n\n", "a")
    elif funcion is not None:
        escribir_tex("\\[\n\\Rightarrow ", "a")
        escribir_tex(sym.latex(funcion)
                     .replace("λ", r"\lambda")
                     .replace(r"\log", r"\ln"), "a")
        escribir_tex("\n\\]\\\\\n\n", "a")
    elif list_:
        escribir_tex("\\[\n\\Rightarrow \\text{"+txt+"}", "a")
        escribir_tex(r"\lambda="+sym.latex(list_[0]), "a")
        for i in range(1, len(list_)):
            escribir_tex(r",\hspace{2mm}", "a")
            escribir_tex(r"\lambda="+sym.latex(list_[i]), "a")
        escribir_tex("\n\\]\\\\\n\n", "a")
