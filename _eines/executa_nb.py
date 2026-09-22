# -*- coding: utf-8 -*-
"""Executa totes les cel.les de codi d'un quadern, en ordre i en un sol espai de noms.

No desa les sortides al fitxer: serveix per comprovar que tot corre abans de
portar-ho a classe, i per veure els numeros reals que sortiran a pantalla.

    CEIABD-IA/.venv/Scripts/python.exe _eines/executa_nb.py "ruta/al/quadern.ipynb"

Surt amb codi 1 si alguna cel.la peta.
"""
import ast
import io
import json
import sys
import traceback

import matplotlib
matplotlib.use("Agg")  # res de finestres

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def executa(ruta, max_sortida=500):
    nb = json.load(io.open(ruta, encoding="utf-8"))
    entorn = {"__name__": "__main__"}
    n_codi = 0
    errors = 0

    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        n_codi += 1
        font = "".join(c["source"])
        print(f"\n----- cel.la {i} -----")
        try:
            arbre = ast.parse(font)
            # Jupyter imprimeix el valor de l'ultima expressio; ho imitem
            if arbre.body and isinstance(arbre.body[-1], ast.Expr):
                cos = ast.Module(body=arbre.body[:-1], type_ignores=[])
                ultima = ast.Expression(body=arbre.body[-1].value)
                exec(compile(cos, "<cell>", "exec"), entorn)
                val = eval(compile(ultima, "<cell>", "eval"), entorn)
                if val is not None:
                    s = str(val)
                    print(s[:max_sortida] + ("..." if len(s) > max_sortida else ""))
            else:
                exec(compile(arbre, "<cell>", "exec"), entorn)
            print("[OK]")
        except Exception:
            errors += 1
            print("[ERROR]")
            traceback.print_exc(limit=4)

    print(f"\n=========== {n_codi} cel.les de codi, {errors} errors ===========")
    return errors


if __name__ == "__main__":
    total = 0
    for ruta in sys.argv[1:]:
        print("=" * 70)
        print(ruta)
        print("=" * 70)
        total += executa(ruta)
    sys.exit(1 if total else 0)
