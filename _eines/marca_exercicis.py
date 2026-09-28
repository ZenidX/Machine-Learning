# -*- coding: utf-8 -*-
"""Marca amb l'etiqueta `exercici` les cel.les que ha d'omplir l'alumne.

Per que existeix: als quaderns de practica, una cel.la d'exercici sol portar els
imports i els comentaris que guien, i sovint referencia una variable que l'alumne
crea a l'exercici anterior. Si s'executa de dalt a baix, peta -- i llavors la
xifra d'errors d'`executa_nb.py` no distingeix una cel.la que espera l'alumne
d'una cel.la de debo trencada.

Amb l'etiqueta, `executa_nb.py` en comprova la sintaxi i no l'executa.

    python marca_exercicis.py <quadern.ipynb> <index> [<index> ...]
    python marca_exercicis.py <quadern.ipynb> --llista

Els indexs son els que imprimeix `--llista`, que son els mateixos que fa servir
`executa_nb.py` als seus missatges (comencant per 1).
"""
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ETIQUETA = "exercici"


def llista(ruta):
    nb = json.load(io.open(ruta, encoding="utf-8"))
    for i, c in enumerate(nb["cells"], 1):
        if c["cell_type"] != "code":
            continue
        font = "".join(c["source"])
        primera = next((l for l in font.split("\n") if l.strip()), "(buida)")
        marca = "[exercici]" if ETIQUETA in c.get("metadata", {}).get("tags", []) else "          "
        print(f"{i:4}  {marca}  {primera[:78]}")
    return 0


def marca(ruta, indexs):
    nb = json.load(io.open(ruta, encoding="utf-8"))
    total = len(nb["cells"])
    fets = []
    for i in indexs:
        if not 1 <= i <= total:
            print(f"index {i} fora de rang (el quadern te {total} cel.les)")
            return 1
        c = nb["cells"][i - 1]
        if c["cell_type"] != "code":
            print(f"la cel.la {i} no es de codi, no la marco")
            return 1
        etiquetes = c.setdefault("metadata", {}).setdefault("tags", [])
        if ETIQUETA not in etiquetes:
            etiquetes.append(ETIQUETA)
            fets.append(i)

    io.open(ruta, "w", encoding="utf-8").write(
        json.dumps(nb, ensure_ascii=False, indent=1))
    print(f"{ruta}: marcades {len(fets)} cel.les noves {fets}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    ruta = sys.argv[1]
    if sys.argv[2] == "--llista":
        sys.exit(llista(ruta))
    sys.exit(marca(ruta, [int(a) for a in sys.argv[2:]]))
