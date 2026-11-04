# -*- coding: utf-8 -*-
"""Afegeix els grafics il.lustratius (dades inventades) a EX_02_cancer.ipynb.

EX_02 no te generador: aquest script llegeix el quadern, treu els grafics que
hi hagues posat abans (cel.les amb l'etiqueta `grafic_il`) i els torna a
inserir just abans de la cel.la de codi de cada exercici (a l'exercici 8, que
no en te, just despres de l'enunciat). Es pot executar tantes vegades com calgui.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_EX_02.py
    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_EX_02.py --neteja

Amb `--neteja` (despres d'executar el quadern amb nbconvert) buida les sortides
de les cel.les d'exercici: l'alumne les ha de trobar sense res.

Regla: els dibuixos ensenyen la idea o com es mesura, mai el resultat amb les
dades de debo. Tots fan servir dades inventades (variables amb sufix _il).
"""
import io
import json
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code

RUTA = "Machine Learning/02_practica/EX_02_cancer.ipynb"
ETIQUETA = "grafic_il"


def marca(cel):
    cel["metadata"] = {"tags": [ETIQUETA]}
    return cel


# exercici -> (markdown, codi)
GRAFICS = {}

GRAFICS[1] = (r"""
Abans de començar, la idea en un dibuix: què vol dir que un conjunt **no està
equilibrat**. Un conjunt inventat de 1.000 correus, amb molts més de normals que de
brossa. La línia discontínua és on hauria d'arribar cada barra si les dues classes
pesessin igual. Quan compteu els valors de `target`, feu-vos aquest dibuix al cap.
""", r"""
import numpy as np
import matplotlib.pyplot as plt

classes_il = ["no és brossa", "és brossa"]          # dades inventades, no són tumors
comptes_il = np.array([780, 220])

fig, ax = plt.subplots(figsize=(7, 4.5))
barres_il = ax.bar(classes_il, comptes_il, color=["tab:blue", "tab:red"], width=0.55)
for barra, n in zip(barres_il, comptes_il):
    ax.text(barra.get_x() + barra.get_width() / 2, n + 15,
            f"{n}  ({100 * n / comptes_il.sum():.0f} %)", ha="center")
ax.axhline(comptes_il.sum() / 2, color="black", linestyle="--", linewidth=1,
           label="si estigués equilibrat (la meitat cadascuna)")
ax.set_ylim(0, 900)
ax.set_ylabel("nombre de mostres")
ax.set_title("Dades inventades: un conjunt desequilibrat")
ax.legend(loc="upper right")
ax.grid(axis="y", alpha=0.3)
plt.show()
""")

GRAFICS[2] = (r"""
Abans de començar, la idea en un dibuix: el que fa `train_test_split` i el que mesura
`.score()`. A dalt, 100 files inventades partides 70/30: el model només veu les
blaves. A sota, les 30 files d'examen, cada una verda si el model l'encerta i vermella
si no. L'exactitud és comptar verds i dividir pel total, res més.
""", r"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

rng = np.random.default_rng(3)
n_il, n_examen_il = 100, 30
encert_il = np.ones(n_examen_il, dtype=bool)
encert_il[rng.choice(n_examen_il, 4, replace=False)] = False   # 4 errors inventats

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 4.2), height_ratios=[1, 1.3])
ax1.add_patch(Rectangle((0, 0), 70, 1, color="tab:blue", alpha=0.7))
ax1.add_patch(Rectangle((70, 0), 30, 1, color="tab:orange", alpha=0.7))
ax1.text(35, 0.5, "entrenament: 70 files (el model aprèn d'aquí)", ha="center", va="center",
         color="white", fontsize=11)
ax1.text(85, 0.5, "examen: 30 files", ha="center", va="center", color="white", fontsize=11)
ax1.set_xlim(0, n_il)
ax1.set_ylim(0, 1)
ax1.axis("off")
ax1.set_title("Dades inventades: test_size=0.3 vol dir el 30 % a l'examen")

for j, ok in enumerate(encert_il):
    ax2.add_patch(Rectangle((j + 0.05, 0.05), 0.9, 0.9,
                            color="tab:green" if ok else "tab:red", alpha=0.8))
    ax2.text(j + 0.5, 0.5, "✓" if ok else "✗", ha="center", va="center", color="white")
ax2.set_xlim(0, n_examen_il)
ax2.set_ylim(0, 1)
ax2.axis("off")
ax2.set_title(f"Les 30 files d'examen: exactitud = {encert_il.sum()} encerts / 30 = "
              f"{encert_il.mean():.2f}".replace(".", ","))
plt.tight_layout()
plt.show()
""")


# matriu inventada que fan servir els dibuixos dels exercicis 3 i 5
MATRIU_IL = r"""
# matriu de confusió INVENTADA: files = real, columnes = predit, ordre [maligne, benigne]
matriu_il = np.array([[40, 6],
                      [4, 50]])
noms_il = ["maligne", "benigne"]
"""

GRAFICS[3] = (r"""
Abans de començar, la idea en un dibuix: com es llegeix una matriu de confusió. Els
números són inventats (100 mostres). Cada fila és el que **era** de veritat i cada
columna el que el model **ha dit**. La diagonal són els encerts; les dues caselles de
fora, els dos tipus d'error. Busqueu la mateixa casella a la vostra matriu.
""", r"""
import numpy as np
import matplotlib.pyplot as plt
""" + MATRIU_IL + r"""
nom_casella_il = [["encert\n(maligne dit maligne)", "FALS NEGATIU\n(maligne dit benigne)"],
                  ["FALS POSITIU\n(benigne dit maligne)", "encert\n(benigne dit benigne)"]]
color_casella_il = [["tab:green", "tab:red"], ["tab:orange", "tab:green"]]

fig, ax = plt.subplots(figsize=(7.5, 6))
for f in range(2):
    for c in range(2):
        ax.add_patch(plt.Rectangle((c, 1 - f), 1, 1, color=color_casella_il[f][c], alpha=0.35))
        ax.text(c + 0.5, 1 - f + 0.62, str(matriu_il[f, c]), ha="center", va="center",
                fontsize=26, fontweight="bold")
        ax.text(c + 0.5, 1 - f + 0.3, nom_casella_il[f][c], ha="center", va="center",
                fontsize=10)
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_xticks([0.5, 1.5], noms_il)
ax.set_yticks([1.5, 0.5], noms_il)
ax.xaxis.tick_top()
ax.xaxis.set_label_position("top")
ax.set_xlabel("PREDIT (columnes)")
ax.set_ylabel("REAL (files)")
ax.set_title(f"Dades inventades: les quatre caselles sumen {matriu_il.sum()}, "
             "totes les mostres de l'examen", pad=40)
for v in (1,):
    ax.axhline(v, color="black", linewidth=1)
    ax.axvline(v, color="black", linewidth=1)
plt.tight_layout()
plt.show()
""")

GRAFICS[4] = (r"""
Abans de començar, la idea en un dibuix: què fa un `DummyClassifier(strategy="most_frequent")`.
A l'esquerra, un entrenament inventat amb dues classes; a la dreta, el que el model diu
per a 30 files d'examen qualssevol. No mira cap columna: mira quina classe surt més a
l'entrenament i la repeteix. Si funciona o no, ho mesureu vosaltres.
""", r"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

entrena_il = {"classe A": 65, "classe B": 35}         # recompte inventat
majoritaria_il = max(entrena_il, key=entrena_il.get)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.8), width_ratios=[1, 2.2])
ax1.bar(list(entrena_il), list(entrena_il.values()), color=["tab:blue", "tab:red"])
ax1.set_title("Entrenament inventat: el que el model compta")
ax1.set_ylabel("files")
ax1.grid(axis="y", alpha=0.3)

for j in range(30):
    ax2.add_patch(Rectangle((j % 15 + 0.05, 1 - j // 15 + 0.05), 0.9, 0.9,
                            color="tab:blue", alpha=0.8))
    ax2.text(j % 15 + 0.5, 1 - j // 15 + 0.5, "A", ha="center", va="center", color="white")
ax2.set_xlim(0, 15)
ax2.set_ylim(0, 2)
ax2.axis("off")
ax2.set_title(f"Les seves 30 prediccions: sempre «{majoritaria_il}», miri el que miri")
plt.tight_layout()
plt.show()
""")

GRAFICS[5] = (r"""
Abans de començar, la idea en un dibuix: les dues mesures són la mateixa casella
dividida per coses diferents. Amb la matriu inventada de l'exercici 3, la
**sensibilitat** divideix per la **fila** del maligne real, i la **precisió del
positiu** per la **columna** del maligne predit. Quina casella d'error entra a cada
denominador, mireu-ho vosaltres al dibuix i a la definició.
""", r"""
import numpy as np
import matplotlib.pyplot as plt
""" + MATRIU_IL + r"""
def dibuixa_matriu_il(ax, ressalta, titol):
    for f in range(2):
        for c in range(2):
            dins = (ressalta == "fila" and f == 0) or (ressalta == "columna" and c == 0)
            color = "tab:green" if (f == 0 and c == 0) else ("tab:blue" if dins else "white")
            ax.add_patch(plt.Rectangle((c, 1 - f), 1, 1, color=color, alpha=0.35 if dins else 1))
            ax.text(c + 0.5, 1 - f + 0.5, str(matriu_il[f, c]), ha="center", va="center",
                    fontsize=22, fontweight="bold" if dins else "normal",
                    color="black" if dins else "gray")
    ax.axhline(1, color="black", linewidth=1)
    ax.axvline(1, color="black", linewidth=1)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5], noms_il)
    ax.set_yticks([1.5, 0.5], noms_il)
    ax.xaxis.tick_top()
    ax.set_xlabel("predit")
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("real")
    ax.set_title(titol, pad=12)

vp_il = matriu_il[0, 0]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))
dibuixa_matriu_il(ax1, "fila", f"Sensibilitat = {vp_il} / suma de la FILA = "
                  f"{vp_il}/{matriu_il[0].sum()} = {vp_il / matriu_il[0].sum():.3f}".replace(".", ","))
dibuixa_matriu_il(ax2, "columna", f"Precisió del positiu = {vp_il} / suma de la COLUMNA = "
                  f"{vp_il}/{matriu_il[:, 0].sum()} = {vp_il / matriu_il[:, 0].sum():.3f}".replace(".", ","))
fig.suptitle("Dades inventades: la casella verda és la mateixa, el denominador no", y=1.02)
plt.tight_layout()
plt.show()
""")

GRAFICS[6] = (r"""
Abans de començar, la idea en un dibuix: una taula amb dues mesures per model es pot
llegir com un pla. Cada punt és un model **inventat**; ordenar per exactitud és llegir-los
d'esquerra a dreta, i ordenar per sensibilitat, de baix a dalt. Feu la mateixa lectura
amb la vostra taula.
""", r"""
import numpy as np
import matplotlib.pyplot as plt

models_il = {"model A": (0.95, 0.94), "model B": (0.93, 0.90),   # (exactitud, sensibilitat)
             "model C": (0.91, 0.86), "model D": (0.88, 0.80)}   # valors inventats

fig, ax = plt.subplots(figsize=(7.5, 5.5))
for nom, (acc, sens) in models_il.items():
    ax.scatter(acc, sens, s=90, color="tab:blue", edgecolor="k", zorder=3)
    ax.annotate(nom, (acc, sens), textcoords="offset points", xytext=(8, 6))
ax.annotate("", xy=(0.97, 0.775), xytext=(0.87, 0.775),
            arrowprops=dict(arrowstyle="->", color="tab:orange", linewidth=2))
ax.text(0.92, 0.78, "ordre per exactitud", color="tab:orange", ha="center")
ax.annotate("", xy=(0.865, 0.96), xytext=(0.865, 0.79),
            arrowprops=dict(arrowstyle="->", color="tab:red", linewidth=2))
ax.text(0.868, 0.875, "ordre per\nsensibilitat", color="tab:red", va="center")
ax.set_xlim(0.86, 0.98)
ax.set_ylim(0.77, 0.97)
ax.set_xlabel("exactitud (accuracy)")
ax.set_ylabel("sensibilitat sobre la classe positiva")
ax.set_title("Dades inventades: dues ordenacions de la mateixa taula")
ax.grid(alpha=0.3)
plt.show()
""")

GRAFICS[7] = (r"""
Abans de començar, la idea en un dibuix: què fa el llindar. Un model inventat dona a
cada tumor una probabilitat de «maligne». Aquí teniu, separades, les probabilitats dels
tumors que **eren** malignes (vermell) i dels que **eren** benignes (blau). Les dues
muntanyes se solapen. La línia vertical és el llindar: tot el que queda a la dreta es
diu «maligne». Les zones ratllades són els errors: malignes a l'esquerra (falsos
negatius) i benignes a la dreta (falsos positius). Què passa amb aquestes dues zones
quan moveu la línia, ho mesureu vosaltres.
""", r"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
p_malignes_il = rng.beta(5, 2, 200)      # probabilitats inventades: els malignes, cap a 1
p_benignes_il = rng.beta(2, 5, 300)      # els benignes, cap a 0
vores_il = np.linspace(0, 1, 41)

fig, ax = plt.subplots(figsize=(9, 4.8))
for llindar_il in [0.5]:
    fn_il = (p_malignes_il < llindar_il).sum()
    fp_il = (p_benignes_il >= llindar_il).sum()
    ax.hist(p_benignes_il, bins=vores_il, color="tab:blue", alpha=0.45, label="eren benignes")
    ax.hist(p_malignes_il, bins=vores_il, color="tab:red", alpha=0.45, label="eren malignes")
    ax.hist(p_malignes_il[p_malignes_il < llindar_il], bins=vores_il, histtype="step",
            hatch="///", color="tab:red", label=f"falsos negatius: {fn_il}")
    ax.hist(p_benignes_il[p_benignes_il >= llindar_il], bins=vores_il, histtype="step",
            hatch="\\\\\\", color="tab:blue", label=f"falsos positius: {fp_il}")
    ax.axvline(llindar_il, color="black", linewidth=2)
    ax.set_ylim(0, 46)
    ax.text(llindar_il + 0.01, 31, "dic «maligne» →", fontsize=9)
    ax.set_title(f"Llindar {llindar_il}".replace(".", ","))
    ax.set_xlabel("probabilitat de «maligne» que dona el model")
    ax.legend(loc="upper left", ncol=2, fontsize=9)
    ax.grid(alpha=0.3)
ax.set_ylabel("nombre de tumors")
fig.suptitle("Dades inventades: el llindar és una línia que talla dues muntanyes que se solapen")
plt.tight_layout()
plt.show()
""")

GRAFICS[8] = (r"""
Abans de decidir, la idea en un dibuix: el llindar no és un sí o un no, és un
**botó que gira**. Amb el mateix model inventat de l'exercici 7, aquí teniu què passa
amb les dues mesures (esquerra) i amb els dos tipus d'error (dreta) per a cada llindar
possible. No hi ha cap llindar que faci zero els dos errors alhora: triar-ne un és
triar quin error accepteu. Els vostres números són els que heu calculat, no aquests.
""", r"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
p_malignes_il = rng.beta(5, 2, 200)      # el mateix model inventat de l'exercici 7
p_benignes_il = rng.beta(2, 5, 300)

llindars_il = np.linspace(0.02, 0.98, 97)
vp_il = np.array([(p_malignes_il >= t).sum() for t in llindars_il])
fp_il = np.array([(p_benignes_il >= t).sum() for t in llindars_il])
fn_il = len(p_malignes_il) - vp_il

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))
ax1.plot(llindars_il, vp_il / len(p_malignes_il), color="tab:red", linewidth=2,
         label="sensibilitat (malignes trobats)")
# on el model no diu "maligne" ni un cop, la precisió del positiu no existeix: no la pintem
precisio_il = np.where(vp_il + fp_il > 0, vp_il / np.maximum(vp_il + fp_il, 1), np.nan)
ax1.plot(llindars_il, precisio_il, color="tab:blue", linewidth=2,
         label="precisió del positiu")
ax1.set_xlabel("llindar (dic «maligne» si P(maligne) ≥ llindar)")
ax1.set_ylim(0, 1.05)
ax1.set_title("Les dues mesures, llindar a llindar")
ax1.legend(loc="lower center")
ax1.grid(alpha=0.3)

ax2.plot(llindars_il, fn_il, color="tab:red", linewidth=2, label="falsos negatius")
ax2.plot(llindars_il, fp_il, color="tab:orange", linewidth=2, label="falsos positius")
ax2.set_xlabel("llindar")
ax2.set_ylabel("nombre de tumors")
ax2.set_title("Els dos errors, llindar a llindar")
ax2.legend(loc="upper center")
ax2.grid(alpha=0.3)
fig.suptitle("Dades inventades: moure el llindar canvia un error per l'altre")
plt.tight_layout()
plt.show()
""")


def insereix():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    cells = [c for c in nb["cells"]
             if ETIQUETA not in c.get("metadata", {}).get("tags", [])]

    nou = []
    pendent = None          # exercici del qual hem vist l'enunciat i encara no el dibuix
    for c in cells:
        text = "".join(c["source"])
        es_exercici = "exercici" in c.get("metadata", {}).get("tags", [])
        if pendent is not None and (es_exercici or pendent == 8):
            # davant del codi de l'exercici (o, al 8, just despres de l'enunciat)
            m, k = GRAFICS[pendent]
            nou += [marca(md(m)), marca(code(k))]
            pendent = None
        nou.append(c)
        if c["cell_type"] == "markdown" and text.startswith("### Exercici "):
            n = int(text.split()[2])
            if n in GRAFICS:
                pendent = n
    if pendent is not None:
        m, k = GRAFICS[pendent]
        nou += [marca(md(m)), marca(code(k))]

    nb["cells"] = nou
    io.open(RUTA, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
    print(f"{sum(1 for c in nou if ETIQUETA in c['metadata'].get('tags', []))} cel.les il.lustratives")


def neteja():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    for c in nb["cells"]:
        if c["cell_type"] == "code" and "exercici" in c.get("metadata", {}).get("tags", []):
            c["outputs"] = []
            c["execution_count"] = None
    io.open(RUTA, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
    print("sortides d'exercici buidades")


if __name__ == "__main__":
    neteja() if "--neteja" in sys.argv else insereix()
