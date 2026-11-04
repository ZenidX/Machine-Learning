# -*- coding: utf-8 -*-
"""Afegeix els dibuixos d'idea (dades inventades) a EX_03, EX_05 i EX_06.

Aquests tres quaderns no tenen generador: aquest script els llegeix, treu les
cel.les que hi havia posat ell mateix (marcades amb `metadata.grafic_il`) i hi
torna a posar les d'ara. Es pot executar tantes vegades com calgui.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_EX_bloc3.py [EX_03 EX_05 EX_06]

On va cada cel.la: just despres de la cel.la de text que comenca amb la clau
(`## Exercici 3`...), o sigui entre l'enunciat i la cel.la de codi buida.

Regla de Xavi: el dibuix ensenya la idea o com es mesura el que es demana,
mai el resultat amb les dades de debo.
"""
import io
import json
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code

MARCA = "grafic_il"
CARPETA = "Machine Learning/02_practica/"


def _marca(c):
    c["metadata"][MARCA] = True
    return c


def aplica(nom, insercions):
    """insercions: llista de (clau_capcalera, [cel.les]). Insereix despres de la capcalera."""
    ruta = CARPETA + nom
    nb = json.load(io.open(ruta, encoding="utf-8"))
    netes = [c for c in nb["cells"] if not c.get("metadata", {}).get(MARCA)]
    sortida, usades = [], set()
    for c in netes:
        sortida.append(c)
        if c["cell_type"] != "markdown":
            continue
        primera = "".join(c["source"]).lstrip().split("\n")[0]
        for clau, noves in insercions:
            if primera.startswith(clau) and clau not in usades:
                usades.add(clau)
                sortida.extend(_marca(x) for x in noves)
    falten = [k for k, _ in insercions if k not in usades]
    if falten:
        raise SystemExit(f"{nom}: no trobo {falten}")
    nb["cells"] = sortida
    io.open(ruta, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    print(f"{nom}: {len(sortida)} cel.les ({len(sortida) - len(netes)} noves)")


PREPARACIO = [
    md(r"""
### Els dibuixos d'aquest quadern

Abans de cada exercici hi ha un dibuix fet amb **dades inventades** (les variables acaben en
`_il`). Ensenya la idea, o com es mesura el que es demana; **no** el resultat. Els números de
debò els heu de treure vosaltres. Executeu aquesta cel·la un cop abans dels dibuixos.
"""),
    code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""),
]


def idea(text):
    return md("Abans de començar, la idea en un dibuix: " + text.strip())


# =====================================================================  EX_03
EX_03 = [
    ("## Els objectes que manegues", PREPARACIO),

    ("## Exercici 1", [
        idea(r"""
com queda una graella d'imatges feta amb `plt.subplots` i `imshow`. Són tres imatges
**inventades** de 8×8 (no són xifres), cadascuna amb el seu títol i sense eixos. Cada imatge és
una matriu de números: 0 és negre i el valor més alt, blanc.
"""),
        code(r"""
creu_il = np.zeros((8, 8))
creu_il[3:5, 1:7] = 16
creu_il[1:7, 3:5] = 16
marc_il = np.zeros((8, 8))
marc_il[[1, 6], 1:7] = 12
marc_il[1:7, [1, 6]] = 12
diag_il = np.diag(np.full(8, 16.0)) + np.diag(np.full(7, 8.0), 1)

fig, axs = plt.subplots(1, 3, figsize=(8, 3))
for ax, img, nom in zip(axs, [creu_il, marc_il, diag_il], ["creu", "marc", "diagonal"]):
    ax.imshow(img, cmap="gray")
    ax.set_title(f"inventada: {nom}")
    ax.axis("off")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 2", [
        idea(r"""
una imatge també és una taula. A dalt, la creu inventada de 8×8 amb el número de cada píxel.
A baix, **la mateixa** imatge desplegada en una sola fila de 64 columnes: les 8 files posades una
darrere l'altra. Les línies de colors marquen on acaba cada fila de la imatge. Res no es perd:
és la mateixa informació amb una altra forma.
"""),
        code(r"""
fila_il = creu_il.reshape(-1)                      # 8x8 -> 64

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6.5), gridspec_kw={"height_ratios": [4, 1]})
ax1.imshow(creu_il, cmap="gray", vmin=0, vmax=16)
for i in range(8):
    for j in range(8):
        ax1.text(j, i, f"{creu_il[i, j]:.0f}", ha="center", va="center",
                 color="black" if creu_il[i, j] > 8 else "white", fontsize=8)
ax1.set_yticks(range(8), [f"fila {i}" for i in range(8)])
ax1.set_xticks(range(8))
ax1.set_title(f"La imatge: forma {creu_il.shape}")

ax2.imshow(fila_il.reshape(1, -1), cmap="gray", vmin=0, vmax=16, aspect="auto")
colors_fila = plt.cm.tab10(np.arange(8))
for k in range(8):
    ax2.axvspan(8 * k - 0.5, 8 * k + 7.5, ymin=0, ymax=0.12, color=colors_fila[k])
    ax2.axvline(8 * k - 0.5, color="tab:red", linewidth=1)
ax2.set_xticks([8 * k + 3.5 for k in range(8)], [f"fila {k}" for k in range(8)])
ax2.set_yticks([])
ax2.set_title(f"La mateixa imatge com una fila de taula: forma {fila_il.shape}")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 3", [
        idea(r"""
com es llegeixen les dues columnes d'exactitud (entrenament i examen) per a uns models
**inventats**, A, B, C i D. El que interessa és la **distància** entre les dues barres de cada
model: el que treu gairebé un 100 % a l'entrenament i força menys a l'examen està memoritzant.
Quin dels vostres cinc ho fa és la vostra troballa.
"""),
        code(r"""
models_il = ["A", "B", "C", "D"]
entrena_il = np.array([0.97, 1.00, 0.99, 0.93])    # números inventats
examen_il = np.array([0.95, 0.84, 0.96, 0.92])

x_il = np.arange(len(models_il))
plt.figure(figsize=(7, 4.2))
plt.bar(x_il - 0.2, entrena_il, width=0.4, color="tab:blue", label="entrenament")
plt.bar(x_il + 0.2, examen_il, width=0.4, color="tab:orange", label="examen")
for xi, a, b in zip(x_il, entrena_il, examen_il):
    plt.annotate("", xy=(xi + 0.2, b), xytext=(xi + 0.2, a),
                 arrowprops=dict(arrowstyle="<->", color="tab:red"))
plt.xticks(x_il, [f"model {m}" for m in models_il])
plt.ylim(0.7, 1.03)
plt.ylabel("exactitud")
plt.title("Dades inventades: la fletxa vermella és el que es perd a l'examen")
plt.legend(loc="lower right")
plt.grid(alpha=0.3, axis="y")
plt.show()
"""),
    ]),

    ("## Exercici 4", [
        idea(r"""
com es llegeix una matriu de confusió, amb 4 classes **inventades** (A, B, C, D) en lloc de 10.
Cada fila és la classe real i cada columna la predita: la diagonal són els encerts. Per trobar la
confusió més freqüent s'esborra la diagonal i es busca el màxim de la resta (el requadre
vermell). Amb els dígits la graella serà de 10×10.
"""),
        code(r"""
classes_il = ["A", "B", "C", "D"]
conf_il = np.array([[48, 1, 0, 1],                 # números inventats
                    [2, 41, 6, 1],
                    [0, 3, 45, 2],
                    [1, 0, 2, 47]])

fora_il = conf_il.copy()
np.fill_diagonal(fora_il, 0)
real_il, pred_il = np.unravel_index(fora_il.argmax(), fora_il.shape)

fig, ax = plt.subplots(figsize=(5.5, 4.8))
ax.imshow(conf_il, cmap="Blues")
for i in range(4):
    for j in range(4):
        ax.text(j, i, conf_il[i, j], ha="center", va="center",
                color="white" if conf_il[i, j] > 25 else "black")
ax.add_patch(plt.Rectangle((pred_il - 0.5, real_il - 0.5), 1, 1, fill=False,
                           edgecolor="tab:red", linewidth=3))
ax.set_xticks(range(4), classes_il)
ax.set_yticks(range(4), classes_il)
ax.set_xlabel("predit")
ax.set_ylabel("real")
ax.set_title(f"Inventada: la confusió més freqüent és real {classes_il[real_il]}, "
             f"predit {classes_il[pred_il]}", fontsize=10)
plt.show()
"""),
    ]),

    ("## Exercici 5", [
        idea(r"""
com es troben els errors. Vint etiquetes reals **inventades** i les vint prediccions d'un model
també inventat, una sota l'altra. Les columnes en vermell són on no coincideixen, i
`np.where(prediccions != reals)[0]` en dona precisament les posicions (el títol).
"""),
        code(r"""
rng = np.random.default_rng(3)
reals_il = rng.integers(0, 10, 20)
predits_il = reals_il.copy()
predits_il[[4, 11, 17]] = [7, 3, 1]                # tres errors inventats
errors_il = np.where(predits_il != reals_il)[0]

fig, ax = plt.subplots(figsize=(12, 2.2))
ax.imshow((predits_il != reals_il).reshape(1, -1).repeat(2, axis=0), cmap="Reds", vmin=0,
          vmax=1.6, aspect="auto")
for j in range(20):
    ax.text(j, 0, reals_il[j], ha="center", va="center")
    ax.text(j, 1, predits_il[j], ha="center", va="center")
ax.set_yticks([0, 1], ["real", "predit"])
ax.set_xticks(range(20))
ax.set_xlabel("posició dins de l'examen")
ax.set_title(f"Dades inventades: errors a les posicions {errors_il.tolist()}")
plt.show()
"""),
    ]),

    ("## Exercici 6", [
        idea(r"""
què fa `SelectKBest` amb una imatge. Una graella **inventada** de 6×6 on cada casella té una
puntuació a l'atzar (a l'esquerra). El selector es queda les 10 caselles amb la puntuació més
alta, i `get_support()` torna un `True` a cada una; amb `.reshape(...)` les tornem a posar al seu
lloc de la imatge (a la dreta). Quins píxels tria amb els dígits, i si serveixen, ho heu de
veure vosaltres.
"""),
        code(r"""
rng = np.random.default_rng(8)
punts_il = rng.random(36)                          # una puntuació inventada per casella
tria_il = np.zeros(36, dtype=bool)
tria_il[np.argsort(punts_il)[-10:]] = True         # les 10 més altes, com get_support()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
im = ax1.imshow(punts_il.reshape(6, 6), cmap="viridis")
fig.colorbar(im, ax=ax1, label="puntuació inventada")
ax1.set_title("La puntuació de cada casella")
ax2.imshow(tria_il.reshape(6, 6), cmap="gray")
ax2.set_title(f"Les {tria_il.sum()} que es queden (blanc = True)")
for ax in (ax1, ax2):
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 7", [
        idea(r"""
com es compta quantes caselles coincideixen entre dues tries. Dues màscares **inventades** de
6×6, cadascuna amb 10 caselles marcades, i a la dreta les que són a totes dues: un `&` entre
màscares i un `.sum()`. El vostre número surt de comparar l'importància del bosc amb el selector
de l'exercici 6.
"""),
        code(r"""
rng = np.random.default_rng(9)
mascara_a_il = np.zeros(36, dtype=bool)
mascara_a_il[rng.choice(36, 10, replace=False)] = True
mascara_b_il = np.zeros(36, dtype=bool)
mascara_b_il[rng.choice(36, 10, replace=False)] = True
les_dues_il = mascara_a_il & mascara_b_il

fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
for ax, m_il, titol in [(axs[0], mascara_a_il, "tria A"), (axs[1], mascara_b_il, "tria B"),
                        (axs[2], les_dues_il, f"a totes dues: {les_dues_il.sum()}")]:
    ax.imshow(m_il.reshape(6, 6), cmap="gray")
    ax.set_title(titol)
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.show()
"""),
    ]),
]


# =====================================================================  EX_05
EX_05 = [
    ("## Els objectes que manegues", PREPARACIO),

    ("## Exercici 1", [
        idea(r"""
el mapa dels nuls d'una taula **inventada** de 15 files i 5 columnes. A l'esquerra,
`taula.isna()` dibuixat: cada casella blanca és un buit. A la dreta, `.isna().sum()`: el
recompte per columna. El vostre diagnòstic és el mateix, amb les columnes del CSV.
"""),
        code(r"""
rng = np.random.default_rng(1)
taula_il = pd.DataFrame(rng.normal(size=(15, 5)), columns=["a", "b", "c", "d", "e"])
for col, n_buits in [("b", 3), ("d", 5)]:
    taula_il.loc[rng.choice(15, n_buits, replace=False), col] = np.nan

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
ax1.imshow(taula_il.isna(), cmap="gray_r", aspect="auto", vmin=0, vmax=1.3)
ax1.set_xticks(range(5), taula_il.columns)
ax1.set_ylabel("fila")
ax1.set_title("taula.isna(): fosc = hi ha un nul")
recompte_il = taula_il.isna().sum()
ax2.bar(recompte_il.index, recompte_il.values, color="tab:orange")
ax2.set_title("taula.isna().sum(): nuls per columna")
ax2.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 2", [
        idea(r"""
el que `fit()` no sap digerir. Una taula **inventada**: les columnes numèriques en blau, una
columna de text en vermell, i les caselles buides (`NaN`) en taronja. Un model de scikit-learn
només accepta la part blava. Quin dels dos problemes el fa petar primer us ho dirà el missatge
d'error.
"""),
        code(r"""
capcalera_il = ["mida", "pes", "color", "preu"]
valors_il = [["3.1", "120", "vermell", "9.5"],
             ["2.7", "NaN", "verd", "8.0"],
             ["3.4", "135", "blau", "NaN"],
             ["2.9", "110", "verd", "7.2"]]
tipus_il = np.array([[0, 0, 1, 0],                 # 0 número, 1 text, 2 buit
                     [0, 2, 1, 0],
                     [0, 0, 1, 2],
                     [0, 0, 1, 0]])
colors_il = plt.matplotlib.colors.ListedColormap(["#c6dbef", "#fcbba1", "#fdd49e"])

fig, ax = plt.subplots(figsize=(6.5, 3))
ax.imshow(tipus_il, cmap=colors_il, vmin=-0.5, vmax=2.5, aspect="auto")
for i, fila in enumerate(valors_il):
    for j, v in enumerate(fila):
        ax.text(j, i, v, ha="center", va="center")
ax.set_xticks(range(4), capcalera_il)
ax.set_yticks([])
ax.xaxis.tick_top()
ax.set_title("Inventada: blau = número, vermell = text, taronja = buit", pad=25)
plt.show()
"""),
    ]),

    ("## Exercici 3", [
        idea(r"""
per què un duplicat espatlla l'examen. Deu files **inventades**, de les quals la 2 i la 7 surten
repetides. En partir a l'atzar, una còpia pot anar a l'entrenament i l'altra a l'examen (línies
vermelles): el model ja ha vist aquella fila abans de ser examinat d'ella.
"""),
        code(r"""
entrena_files_il = [0, 1, 2, 3, 5, 6, 7, 8, 9]     # una partició inventada
examen_files_il = [4, 7, 2]                       # 7 i 2 són les còpies

fig, ax = plt.subplots(figsize=(6, 5))
for y, f in enumerate(entrena_files_il):
    ax.text(0, -y, f"fila {f}", ha="center", va="center",
            bbox=dict(facecolor="#c6dbef", edgecolor="tab:blue"))
for y, f in enumerate(examen_files_il):
    ax.text(1, -y * 3, f"fila {f}", ha="center", va="center",
            bbox=dict(facecolor="#fdd49e", edgecolor="tab:orange"))
for y2, f in enumerate(examen_files_il):
    if f in entrena_files_il:
        y1 = entrena_files_il.index(f)
        ax.plot([0.12, 0.88], [-y1, -y2 * 3], color="tab:red", linewidth=2)
ax.text(0, 1.2, "entrenament", ha="center", fontweight="bold")
ax.text(1, 1.2, "examen", ha="center", fontweight="bold")
ax.set_xlim(-0.4, 1.4)
ax.set_ylim(-9, 2)
ax.axis("off")
ax.set_title("Dades inventades: la mateixa fila a tots dos costats")
plt.show()
"""),
    ]),

    ("## Exercici 4", [
        idea(r"""
per què la mitjana i la mediana no omplen igual. Una columna **inventada** amb uns quants valors
molt grans (cua a la dreta). La mitjana (vermell) s'estira cap a la cua; la mediana (verd) es
queda al mig de la majoria. Si una columna és així, omplir amb una o amb l'altra no és el mateix.
Com són les columnes del vi, i si es nota a l'exactitud, és cosa vostra.
"""),
        code(r"""
rng = np.random.default_rng(2)
columna_il = np.concatenate([rng.normal(10, 2, 180), rng.normal(35, 5, 20)])  # cua inventada

plt.figure(figsize=(8, 4))
plt.hist(columna_il, bins=40, color="tab:blue", alpha=0.7)
plt.axvline(columna_il.mean(), color="tab:red", linewidth=2.5,
            label=f"mitjana = {columna_il.mean():.1f}")
plt.axvline(np.median(columna_il), color="tab:green", linewidth=2.5,
            label=f"mediana = {np.median(columna_il):.1f}")
plt.xlabel("valor de la columna inventada")
plt.ylabel("files")
plt.title("Dades inventades: amb una cua, la mitjana se'n va")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""),
    ]),

    ("## Exercici 5", [
        idea(r"""
què fa la codificació *one-hot* amb una columna de text **inventada**, `color`, amb tres valors.
Una columna de text es converteix en tantes columnes com valors diferents, i a cada fila hi ha
un 1 a la del seu valor i 0 a les altres.
"""),
        code(r"""
color_il = pd.Series(["vermell", "verd", "blau", "verd", "vermell", "blau"], name="color")
onehot_il = pd.get_dummies(color_il, prefix="color").astype(int)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1, 3]})
ax1.imshow(np.zeros((6, 1)), cmap="gray_r", vmin=0, vmax=1, aspect="auto")
for i, v in enumerate(color_il):
    ax1.text(0, i, v, ha="center", va="center")
ax1.set_xticks([0], ["color"])
ax1.set_yticks(range(6))
ax1.set_title("abans: 1 columna de text")
ax2.imshow(onehot_il.to_numpy(), cmap="Blues", vmin=0, vmax=1.5, aspect="auto")
for i in range(6):
    for j in range(3):
        ax2.text(j, i, onehot_il.iloc[i, j], ha="center", va="center")
ax2.set_xticks(range(3), onehot_il.columns)
ax2.set_yticks([])
ax2.set_title("després: 3 columnes de 0 i 1")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 6", [
        idea(r"""
primer, el camí de les dades dins del `Pipeline`. El `fit` del pipeline només rep les files
d'entrenament, i cada pas aprèn d'elles (la mediana, les categories). L'examen passa pel mateix
camí més tard, amb `transform`, sense que ningú hi torni a aprendre res.
"""),
        code(r"""
fig, ax = plt.subplots(figsize=(12, 3.6))
ax.axis("off")
caixes_il = [(0.06, 0.5, "CSV sense\nduplicats", "#eeeeee"),
             (0.24, 0.5, "train_test_split", "#eeeeee"),
             (0.46, 0.78, "imputar (num)\nmediana", "#c6dbef"),
             (0.46, 0.22, "one-hot (text)\ncategories", "#c6dbef"),
             (0.68, 0.5, "model", "#fdd49e"),
             (0.88, 0.5, ".score(examen)", "#eeeeee")]
for x, y, text, color in caixes_il:
    ax.text(x, y, text, ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor=color, edgecolor="gray"))
fletxes_il = [((0.11, 0.5), (0.18, 0.5)), ((0.30, 0.55), (0.40, 0.75)),
              ((0.30, 0.45), (0.40, 0.25)), ((0.52, 0.75), (0.63, 0.55)),
              ((0.52, 0.25), (0.63, 0.45)), ((0.72, 0.5), (0.81, 0.5))]
for a, b in fletxes_il:
    ax.annotate("", xy=b, xytext=a, xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", lw=1.5))
ax.add_patch(plt.Rectangle((0.37, 0.05), 0.36, 0.92, transform=ax.transAxes, fill=False,
                           linestyle="--", edgecolor="tab:blue"))
ax.text(0.55, 1.0, "Pipeline: .fit() només amb l'entrenament", transform=ax.transAxes,
        ha="center", color="tab:blue")
ax.set_title("El camí de les dades (esquema)", y=1.08)
plt.show()
"""),
        md(r"""
I la fuita, dibuixada. Una columna **inventada** de 30 valors, ja partida: en blau les files
d'entrenament i en taronja les d'examen. Si la mediana per omplir els buits es calcula **abans**
de partir (línia negra), fa servir també els valors de l'examen; si es calcula **després**,
només amb l'entrenament (línia blava). Són dues medianes diferents, i la comprovació del punt 4
consisteix a mirar quina de les dues ha quedat desada dins del pipeline.
"""),
        code(r"""
rng = np.random.default_rng(8)
valors_col_il = rng.normal(50, 12, 30)
es_examen_il = np.zeros(30, dtype=bool)
es_examen_il[rng.choice(30, 9, replace=False)] = True

med_tot_il = np.median(valors_col_il)
med_entrena_il = np.median(valors_col_il[~es_examen_il])

plt.figure(figsize=(9, 2.8))
plt.scatter(valors_col_il[~es_examen_il], np.zeros((~es_examen_il).sum()), color="tab:blue",
            s=60, label="entrenament")
plt.scatter(valors_col_il[es_examen_il], np.zeros(es_examen_il.sum()), color="tab:orange",
            s=60, marker="s", label="examen")
plt.axvline(med_tot_il, color="black", linestyle="--",
            label=f"mediana abans de partir: {med_tot_il:.2f} (fuita)")
plt.axvline(med_entrena_il, color="tab:blue",
            label=f"mediana només d'entrenament: {med_entrena_il:.2f}")
plt.yticks([])
plt.xlabel("valor de la columna inventada")
plt.title("Dades inventades: on s'ajusta, canvia el que s'aprèn")
plt.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9)
plt.grid(alpha=0.3, axis="x")
plt.show()
"""),
    ]),

    ("## Exercici 7", [
        idea(r"""
quant pesa una sola fila a l'examen. Amb $n$ files d'examen, l'exactitud només pot valer
$0/n, 1/n, \dots, n/n$: cada ratlla és un valor possible. Amb 50 files **inventades**, d'una
ratlla a la següent hi ha 2 punts d'exactitud, i dos resultats que es diferencien en una ratlla
són una sola fila mal classificada.
"""),
        code(r"""
fig, ax = plt.subplots(figsize=(10, 2.6))
for y, n_il in [(1, 50), (0, 40)]:
    possibles_il = np.arange(n_il + 1) / n_il
    possibles_il = possibles_il[possibles_il >= 0.85]
    ax.scatter(possibles_il, np.full(len(possibles_il), y), marker="|", s=400, color="tab:blue")
ax.scatter([47 / 50, 48 / 50], [1, 1], s=120, color="tab:red", zorder=3,
           label="dos resultats inventats: 47/50 i 48/50")
ax.set_yticks([0, 1], ["40 files d'examen", "50 files d'examen"])
ax.set_ylim(-0.6, 1.6)
ax.set_xlabel("exactitud possible")
ax.set_title("Dades inventades: l'exactitud va a salts d'una fila")
ax.legend(loc="lower left", fontsize=9)
ax.grid(alpha=0.3, axis="x")
plt.show()
"""),
    ]),
]


# =====================================================================  EX_06
EX_06 = [
    ("## Els objectes que manegues", PREPARACIO),

    ("## Exercici 1", [
        idea(r"""
els tres passos sobre sis punts **inventats** (no són els de la joguina) i dos centres. Cada
punt va al centre més proper i pren el seu color; el número de cada segment és la distància
**al quadrat** fins al seu centre, i la inèrcia és la suma d'aquests números.
"""),
        code(r"""
X_il = np.array([[0.0, 0.5], [1.0, 0.0], [0.5, 1.5], [4.0, 3.0], [5.0, 4.0], [3.0, 3.5]])
M_il = np.array([[0.0, 0.0], [4.0, 4.0]])

d2_il = np.array([[((x - m) ** 2).sum() for m in M_il] for x in X_il])   # amb bucles, a posta
et_il = d2_il.argmin(axis=1)
colors_il = np.array(["tab:blue", "tab:orange"])

plt.figure(figsize=(6.5, 5.5))
for x, c in zip(X_il, et_il):
    plt.plot([x[0], M_il[c, 0]], [x[1], M_il[c, 1]], color=colors_il[c], linewidth=1.5)
    mig = (x + M_il[c]) / 2
    plt.text(mig[0], mig[1], f"{((x - M_il[c]) ** 2).sum():.2f}", fontsize=9,
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.8))
plt.scatter(X_il[:, 0], X_il[:, 1], c=colors_il[et_il], s=60, edgecolor="k", zorder=3)
plt.scatter(M_il[:, 0], M_il[:, 1], c="black", marker="X", s=200, edgecolor="white", zorder=3)
plt.gca().set_aspect("equal")
plt.title(f"Dades inventades: J = suma dels números = {d2_il.min(axis=1).sum():.2f}")
plt.grid(alpha=0.3)
plt.show()
"""),
    ]),

    ("## Exercici 2", [
        idea(r"""
com es mouen els centres ronda a ronda sobre tres núvols **inventats**. Cada línia negra és el
camí d'un centre, des de la sortida (cercle blanc) fins on s'atura (creu); a la dreta, la inèrcia
després de cada ronda, que mai no puja. Per fer el dibuix sense escriure el bucle, aquí cridem
`KMeans` amb `max_iter=1` una vegada i una altra; el bucle de debò l'escriviu vosaltres.
"""),
        code(r"""
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X_il2, _ = make_blobs(n_samples=150, centers=3, cluster_std=0.9, random_state=12)
M_ara_il = X_il2[[0, 1, 2]].copy()                  # tres punts com a centres de sortida
cami_il, J_il = [M_ara_il], []
for _ in range(8):
    km_il = KMeans(n_clusters=3, init=M_ara_il, n_init=1, max_iter=1).fit(X_il2)
    M_ara_il = km_il.cluster_centers_
    cami_il.append(M_ara_il)
    J_il.append(km_il.inertia_)
cami_il = np.array(cami_il)                         # (rondes, 3, 2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
ax1.scatter(X_il2[:, 0], X_il2[:, 1], c=km_il.labels_, cmap="tab10", vmin=0, vmax=9, s=14, alpha=0.5)
for j in range(3):
    ax1.plot(cami_il[:, j, 0], cami_il[:, j, 1], "o-", color="black", markersize=4)
    ax1.scatter(*cami_il[0, j], s=90, color="white", edgecolor="black", zorder=3)
    ax1.scatter(*cami_il[-1, j], marker="X", s=180, color="black", edgecolor="white", zorder=3)
ax1.set_title("Dades inventades: el camí de cada centre")
ax1.grid(alpha=0.3)
ax2.plot(range(1, len(J_il) + 1), J_il, "o-", color="tab:blue")
ax2.set_xlabel("ronda")
ax2.set_ylabel("inèrcia")
ax2.set_title("La inèrcia de cada ronda")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 3", [
        idea(r"""
com es llegeixen les dues corbes, amb quatre núvols **inventats** i ben separats (a l'esquerra).
La inèrcia baixa sempre; el que es mira és on deixa de baixar de pressa (el colze). La silueta
no baixa sola: es mira on és més alta. Amb dades de joguina com aquestes les dues corbes es
posen d'acord; amb el vi potser no, i llavors la decisió és vostra.
"""),
        code(r"""
from sklearn.metrics import silhouette_score

X_il3, _ = make_blobs(n_samples=300, centers=4, cluster_std=1.0, random_state=7)
ks_il = range(1, 9)
inercies_il, siluetes_il = [], []
for k in ks_il:
    km_il3 = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_il3)
    inercies_il.append(km_il3.inertia_)
    if k >= 2:
        siluetes_il.append(silhouette_score(X_il3, km_il3.labels_))

fig, axs = plt.subplots(1, 3, figsize=(15, 4))
axs[0].scatter(X_il3[:, 0], X_il3[:, 1], s=10, color="gray")
axs[0].set_title("Les dades inventades")
axs[1].plot(list(ks_il), inercies_il, "o-", color="tab:blue")
axs[1].set_xlabel("$k$")
axs[1].set_title("Inèrcia: busqueu el colze")
axs[2].plot(range(2, 9), siluetes_il, "o-", color="tab:green")
axs[2].set_xlabel("$k$")
axs[2].set_title("Silueta: busqueu el màxim")
for ax in axs:
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 4", [
        idea(r"""
què hi ha dins de `.transform(X)`. Vuit punts **inventats** i tres centres: una fila per punt,
una columna per centre, i a cada casella la distància (sense elevar al quadrat). El requadre
vermell de cada fila és el mínim, i la columna on cau és l'etiqueta del punt (a la dreta).
"""),
        code(r"""
X_il4, _ = make_blobs(n_samples=8, centers=3, cluster_std=1.0, random_state=3)
km_il4 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_il4)
T_il = km_il4.transform(X_il4)                      # (8, 3)

fig, ax = plt.subplots(figsize=(5.5, 5.5))
ax.imshow(T_il, cmap="Blues_r", aspect="auto")
for i in range(8):
    for j in range(3):
        ax.text(j, i, f"{T_il[i, j]:.1f}", ha="center", va="center",
                color="white" if T_il[i, j] < 0.4 * T_il.max() else "black")
    j_min = T_il[i].argmin()
    ax.add_patch(plt.Rectangle((j_min - 0.5, i - 0.5), 1, 1, fill=False, edgecolor="tab:red",
                               linewidth=2.5))
    ax.text(3.0, i, f"etiqueta {km_il4.labels_[i]}", va="center")
ax.set_xticks(range(3), [f"centre {j}" for j in range(3)])
ax.set_yticks(range(8), [f"punt {i}" for i in range(8)])
ax.set_xlim(-0.5, 3.9)
ax.set_title("Dades inventades: transform(X), fila a fila")
plt.show()
"""),
    ]),

    ("## Exercici 5", [
        idea(r"""
per què el número del grup no vol dir res. Una taula de grups contra classes **inventada**, i la
mateixa amb els grups renombrats: les files canvien d'ordre, però qui va amb qui no canvia, i per
això l'ARI és idèntic. Una taula bona té, a cada fila, gairebé tot en una sola casella.
"""),
        code(r"""
from sklearn.metrics import adjusted_rand_score

rng = np.random.default_rng(5)
classe_il = np.repeat([0, 1, 2], 30)
grup_il = np.array([2, 0, 1])[classe_il]                # els grups, amb uns altres noms
canvia_il = rng.choice(90, 12, replace=False)
grup_il[canvia_il] = rng.integers(0, 3, 12)              # una mica de barreja inventada
renombrat_il = np.array([1, 2, 0])[grup_il]

fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, g_il, titol in [(axs[0], grup_il, "grups tal com surten"),
                        (axs[1], renombrat_il, "els mateixos, renombrats")]:
    taula_il = pd.crosstab(g_il, classe_il).to_numpy()
    ax.imshow(taula_il, cmap="Blues")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, taula_il[i, j], ha="center", va="center",
                    color="white" if taula_il[i, j] > 15 else "black")
    ax.set_xticks(range(3))
    ax.set_yticks(range(3))
    ax.set_xlabel("classe real")
    ax.set_ylabel("grup")
    ax.set_title(f"{titol}\nARI = {adjusted_rand_score(classe_il, g_il):.4f}")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 6", [
        idea(r"""
per què un centre de k-means es pot dibuixar com una imatge. Sis imatges **inventades** de 8×8:
la mateixa creu, cada cop una mica moguda i amb soroll. El centre d'un grup és la **mitjana**
píxel a píxel de les seves imatges (la de la dreta): una imatge borrosa amb la forma que
comparteixen. Amb els dígits, cada centre serà la «xifra mitjana» del seu grup.
"""),
        code(r"""
rng = np.random.default_rng(2)
creu_il = np.zeros((8, 8))
creu_il[3:5, 1:7] = 16
creu_il[1:7, 3:5] = 16
imatges_il = []
for _ in range(6):
    desp = rng.integers(-1, 2, size=2)
    img = np.roll(creu_il, desp, axis=(0, 1)) + rng.normal(0, 2, (8, 8))
    imatges_il.append(np.clip(img, 0, 16))
centre_il = np.mean(imatges_il, axis=0)

fig, axs = plt.subplots(1, 7, figsize=(14, 2.6))
for ax, img in zip(axs[:6], imatges_il):
    ax.imshow(img, cmap="gray", vmin=0, vmax=16)
    ax.axis("off")
axs[6].imshow(centre_il, cmap="gray", vmin=0, vmax=16)
axs[6].set_title("la mitjana", color="tab:red")
axs[6].axis("off")
fig.suptitle("Dades inventades: sis imatges del mateix grup i el seu centre")
plt.tight_layout()
plt.show()
"""),
    ]),

    ("## Exercici 7", [
        idea(r"""
una foto com una taula de colors. Una imatge **inventada** de 40×40 píxels (cel, sol i herba,
amb soroll). Al mig, cada píxel com un punt segons el seu vermell i el seu verd: els colors de la
foto formen núvols, i k-means hi posa un centre a cadascun. A la dreta, la foto repintada amb
només els colors dels 3 centres.
"""),
        code(r"""
rng = np.random.default_rng(0)
foto_il = np.zeros((40, 40, 3))
foto_il[:25] = [0.45, 0.65, 0.95]                    # cel
foto_il[25:] = [0.25, 0.6, 0.2]                       # herba
yy, xx = np.mgrid[:40, :40]
foto_il[(yy - 10) ** 2 + (xx - 28) ** 2 < 30] = [0.98, 0.85, 0.2]   # sol
foto_il = np.clip(foto_il + rng.normal(0, 0.05, foto_il.shape), 0, 1)

pixels_il = foto_il.reshape(-1, 3)                    # (1600, 3): una fila per píxel
km_il7 = KMeans(n_clusters=3, n_init=4, random_state=42).fit(pixels_il)
repintada_il = km_il7.cluster_centers_[km_il7.labels_].reshape(foto_il.shape)

fig, axs = plt.subplots(1, 3, figsize=(14, 4.4))
axs[0].imshow(foto_il)
axs[0].set_title("La foto inventada")
axs[0].axis("off")
axs[1].scatter(pixels_il[:, 0], pixels_il[:, 1], c=pixels_il, s=6)
axs[1].scatter(km_il7.cluster_centers_[:, 0], km_il7.cluster_centers_[:, 1], marker="X", s=200,
               color="black", edgecolor="white")
axs[1].set_xlabel("vermell")
axs[1].set_ylabel("verd")
axs[1].set_title("Cada píxel, un punt; les creus, els centres")
axs[1].grid(alpha=0.3)
axs[2].imshow(repintada_il)
axs[2].set_title("Repintada amb 3 colors")
axs[2].axis("off")
plt.tight_layout()
plt.show()
"""),
    ]),
]


QUADERNS = {"EX_03": ("EX_03_digits.ipynb", EX_03),
            "EX_05": ("EX_05_dades_brutes.ipynb", EX_05),
            "EX_06": ("EX_06_kmeans.ipynb", EX_06)}

if __name__ == "__main__":
    for clau in sys.argv[1:] or list(QUADERNS):
        aplica(*QUADERNS[clau])
