# -*- coding: utf-8 -*-
"""Treu dels quaderns executats les sortides de ipywidgets i l'estat desat dels controls.

Per que existeix: un quadern executat amb nbconvert desa els controls lliscants
(ipywidgets) dins del fitxer. Colab els pinta en obrir-lo, i es poden arrossegar,
pero no estan connectats a cap kernel: el grafic no es mou. Sembla que el quadern
estigui trencat. Sense la sortida desada, la cel.la apareix buida fins que
s'executa, i llavors els controls funcionen de debo.

    python _eines/treu_widgets.py "ruta/al/quadern.ipynb" [...]
"""
import io
import json
import sys

WIDGET = "application/vnd.jupyter.widget-view+json"


def neteja(ruta):
    nb = json.load(io.open(ruta, encoding="utf-8"))
    tretes = 0
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        abans = len(c.get("outputs", []))
        c["outputs"] = [o for o in c.get("outputs", []) if WIDGET not in o.get("data", {})]
        tretes += abans - len(c["outputs"])
    nb.get("metadata", {}).pop("widgets", None)
    io.open(ruta, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    return tretes


if __name__ == "__main__":
    for r in sys.argv[1:]:
        print(r, "->", neteja(r), "sortides de controls tretes")
