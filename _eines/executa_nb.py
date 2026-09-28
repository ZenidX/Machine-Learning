# -*- coding: utf-8 -*-
"""Executa totes les cel.les de codi d'un quadern, en ordre i en un sol espai de noms.

No desa les sortides al fitxer: serveix per comprovar que tot corre abans de
portar-ho a classe, i per veure els numeros reals que sortiran a pantalla.

Les cel.les marcades amb l'etiqueta `exercici` (a `metadata.tags`) son les que
ha d'omplir l'alumne: es comproven nomes de sintaxi i NO s'executen, perque
referencien variables que encara no existeixen. Aixi la xifra d'errors torna a
voler dir alguna cosa. Per marcar-les hi ha `_eines/marca_exercicis.py`.

Compte amb un parany del backend Agg: matplotlib no dibuixa res fins que algu
li ho demana, aixi que una etiqueta amb LaTeX mal escrit (mathtext) NO peta en
executar la cel.la; petaria a classe, en mostrar la figura. Per aixo, despres de
cada cel.la, aquest script força el dibuix de les figures obertes.

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

import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def dibuixa_figures():
    """Força el render de les figures obertes i les tanca. Retorna quantes eren.

    Es el que fa esclatar un `$\alpha$` mal tancat o una ordre de LaTeX que
    mathtext no coneix: sense aixo, el quadern passa i la figura peta a classe.
    """
    nums = plt.get_fignums()
    for n in nums:
        plt.figure(n).canvas.draw()
    plt.close("all")
    return len(nums)


def executa(ruta, max_sortida=500):
    nb = json.load(io.open(ruta, encoding="utf-8"))
    entorn = {"__name__": "__main__"}
    n_codi = 0
    n_exercici = 0
    errors = 0

    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        font = "".join(c["source"])

        # Cel.la que ha d'omplir l'alumne: es comprova la sintaxi i prou. Sovint
        # referencia variables que l'alumne crea a l'exercici anterior, aixi que
        # executar-la nomes embrutaria el recompte d'errors.
        if "exercici" in c.get("metadata", {}).get("tags", []):
            n_exercici += 1
            print(f"\n----- cel.la {i} (exercici, no s'executa) -----")
            try:
                ast.parse(font)
                print("[sintaxi OK]")
            except SyntaxError:
                errors += 1
                print("[ERROR DE SINTAXI]")
                traceback.print_exc(limit=2)
            continue

        n_codi += 1
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

        # Amb Agg les figures no es dibuixen soles: un mathtext trencat a una
        # etiqueta nomes peta aqui, i a classe petaria en projectar-la.
        try:
            n_fig = dibuixa_figures()
            if n_fig:
                print(f"[{n_fig} figura(es) dibuixada(es)]")
        except Exception:
            errors += 1
            print("[ERROR EN DIBUIXAR LA FIGURA]")
            traceback.print_exc(limit=4)
            plt.close("all")

    resum = f"{n_codi} cel.les de codi, {errors} errors"
    if n_exercici:
        resum += f" (+ {n_exercici} d'exercici, nomes sintaxi)"
    print(f"\n=========== {resum} ===========")
    return errors


if __name__ == "__main__":
    total = 0
    for ruta in sys.argv[1:]:
        print("=" * 70)
        print(ruta)
        print("=" * 70)
        total += executa(ruta)
    sys.exit(1 if total else 0)
