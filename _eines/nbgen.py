# -*- coding: utf-8 -*-
"""Eines per generar i verificar els quaderns del bloc de Machine Learning.

Per que existeix aixo: escriure un .ipynb a ma es propens a errors. El format
demana que cada linia de `source` acabi en \\n excepte l'ultima; si no, les
linies es peguen i el quadern no s'executa encara que el JSON sigui valid.

Us tipic, des d'un script generador:

    from nbgen import md, code, escriu
    cells = [md("# Titol"), code("print('hola')")]
    escriu(cells, "Machine Learning/01_teoria/ML_01_knn.ipynb")
"""
import io
import json
import os


def _linies(s):
    """Parteix un text en linies amb el salt inclos, com vol el format .ipynb."""
    parts = s.strip("\n").split("\n")
    if not parts:
        return []
    return [l + "\n" for l in parts[:-1]] + [parts[-1]]


def md(s):
    """Cel.la de text (Markdown)."""
    return {"cell_type": "markdown", "metadata": {}, "source": _linies(s)}


def code(s):
    """Cel.la de codi, sense sortides desades."""
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": _linies(s)}


def escriu(cells, desti, titol_colab=None):
    """Desa la llista de cel.les com a quadern a `desti`."""
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "colab": {"provenance": [], "name": titol_colab or os.path.basename(desti)},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    carpeta = os.path.dirname(desti)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    io.open(desti, "w", encoding="utf-8").write(
        json.dumps(nb, ensure_ascii=False, indent=1))
    n_codi = sum(1 for c in cells if c["cell_type"] == "code")
    return {"desti": desti, "cel_les": len(cells), "codi": n_codi}
