# -*- coding: utf-8 -*-
"""Afegeix el grafic de les cinc formes i els il.lustratius d'exercici a EX_04_fronteres.ipynb.

El quadern no te generador: aquest script el llegeix, treu les cel.les que ell
mateix havia afegit abans (marcades amb metadata["grafic"] = "EX_04") i les
torna a inserir darrere de les cel.les d'ancoratge. Es pot executar tantes
vegades com calgui.

Regla: els dibuixos fan servir dades INVENTADES (sufix _il) i ensenyen l'eina o
com es mesura el que es demana, mai el resultat amb blobs/moons/circles.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_EX_04.py
"""
import io
import json
import sys

sys.path.insert(0, "_eines")
from nbgen import md, code  # noqa: E402

RUTA = "Machine Learning/02_practica/EX_04_fronteres.ipynb"
MARCA = "EX_04"


def M(s):
    c = md(s)
    c["metadata"]["grafic"] = MARCA
    return c


def C(s):
    c = code(s)
    c["metadata"]["grafic"] = MARCA
    return c


INSERCIONS = []

# ---------------------------------------------------------- exercicis
INSERCIONS.append(("## Exercici 1 — Fabricar i mirar", [
    M(r"""
Abans de començar, la idea en un dibuix: així ha de quedar una figura d'1 fila x 3
columnes, amb un `scatter` a cada `Axes` pintat pel seu `y`. Les formes d'aquí són
**inventades** (franges, quadrants, espiral) i no són les vostres.
"""),
    C(r"""
rng = np.random.default_rng(1)
n_il = 300
# franges en diagonal
A_il = rng.uniform(-2, 2, (n_il, 2))
yA_il = (np.floor((A_il[:, 0] + A_il[:, 1]) / 1.5) % 2).astype(int)
# quadrants (com un tauler d'escacs de 2x2)
B_il = rng.uniform(-2, 2, (n_il, 2))
yB_il = ((B_il[:, 0] > 0) ^ (B_il[:, 1] > 0)).astype(int)
# espiral doble
t_il = rng.uniform(0.5, 3 * np.pi, n_il)
s_il = rng.integers(0, 2, n_il)
C_il = np.column_stack([t_il * np.cos(t_il + np.pi * s_il), t_il * np.sin(t_il + np.pi * s_il)])
C_il += rng.normal(0, 0.3, C_il.shape)

fig, axs = plt.subplots(1, 3, figsize=(14, 4.2))
for ax, (Xd, yd, nom) in zip(axs, [(A_il, yA_il, "franges"), (B_il, yB_il, "quadrants"),
                                    (C_il, s_il, "espiral")]):
    ax.scatter(Xd[:, 0], Xd[:, 1], c=yd, cmap="coolwarm", edgecolors="k", s=15)
    ax.set_title(f"inventat: {nom}")
    ax.grid(alpha=0.3)
fig.suptitle("Una figura 1x3: cada panell, un conjunt pintat pel seu y")
plt.tight_layout()
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 2 — Blobs, el cas fàcil", [
    M(r"""
Abans de començar, la idea en un dibuix: què fa per dins `dibuixa_frontera`. Aquí el
«model» és una regla inventada (*classe 1 si $x_2 > \sin(x_1)$*), escrita com una classe
amb un mètode `predict`, que és l'únic que `dibuixa_frontera` li demana. A l'esquerra,
els punts. Al mig, una graella gruixuda: cada punt de la graella pintat amb el que diu
`predict`. A la dreta, la graella de 300 x 300 de `dibuixa_frontera`, amb `contourf`:
els punts de la graella són tan junts que ja es veuen com una regió.
"""),
    C(r"""
class ReglaInventada:
    # Un model de mentida: només té predict, que és el que necessita dibuixa_frontera
    def predict(self, X):
        return (X[:, 1] > np.sin(X[:, 0])).astype(int)


rng = np.random.default_rng(2)
X_il = rng.uniform(-3, 3, (80, 2))
regla_il = ReglaInventada()
y_il = regla_il.predict(X_il)

fig, axs = plt.subplots(1, 3, figsize=(14, 4.2))
axs[0].scatter(X_il[:, 0], X_il[:, 1], c=y_il, cmap="coolwarm", edgecolors="k", s=15)
axs[0].set_title("1. les dades")

g1_il, g2_il = np.meshgrid(np.linspace(-3.5, 3.5, 15), np.linspace(-3.5, 3.5, 15))
graella_il = np.c_[g1_il.ravel(), g2_il.ravel()]
axs[1].scatter(graella_il[:, 0], graella_il[:, 1], c=regla_il.predict(graella_il),
               cmap="coolwarm", marker="s", s=40, alpha=0.5)
axs[1].scatter(X_il[:, 0], X_il[:, 1], c=y_il, cmap="coolwarm", edgecolors="k", s=15)
axs[1].set_title("2. graella 15 x 15: predict a cada punt")

dibuixa_frontera(axs[2], regla_il, X_il, y_il)
axs[2].set_title("3. graella 300 x 300 amb contourf")
for ax in axs[:2]:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 3 — Moons, el cas que trenca la recta", [
    M(r"""
Abans de començar, la idea en un dibuix: com es comprova «un model s'equivoca en
aquesta zona». Dades inventades (dos núvols que es toquen) i una frontera inventada.
`model.predict(X_te) != y_te` dona un `True` a cada punt mal classificat; aquí estan
marcats amb una creu, i `.sum()` els compta.
"""),
    C(r"""
rng = np.random.default_rng(3)
X_il = np.vstack([rng.normal([0, 0], 1.0, (40, 2)), rng.normal([2, 1.5], 1.0, (40, 2))])
y_il = np.array([0] * 40 + [1] * 40)


class FronteraInventada:
    def predict(self, X):
        return (X[:, 0] + X[:, 1] > 1.8).astype(int)


mal_il = FronteraInventada().predict(X_il) != y_il

fig, ax = plt.subplots(figsize=(6.5, 5))
dibuixa_frontera(ax, FronteraInventada(), X_il, y_il)
ax.scatter(X_il[mal_il, 0], X_il[mal_il, 1], marker="x", color="black", s=110, linewidths=2,
           label="predict != y")
ax.set_title(f"Dades inventades: (predict != y).sum() = {mal_il.sum()} de {len(y_il)}")
ax.legend(loc="upper left")
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 4 — L'escala de l'arbre", [
    M(r"""
Abans de començar, la idea en un dibuix: com compta les fulles un arbre. Cada tall és
«aquesta columna és més gran que tal número», i parteix una regió en dues. Aquí els talls
estan **posats a mà** sobre punts inventats (no és cap arbre entrenat): amb profunditat 1
hi ha un sol tall i 2 fulles; amb profunditat 2, cada meitat es pot tornar a partir, i
surten fins a 4 fulles. Cada fulla és un rectangle, i és per això que la frontera d'un
arbre fa escales.
"""),
    C(r"""
rng = np.random.default_rng(6)
X_il = rng.uniform(0, 10, (60, 2))

fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
colors_il = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

# profunditat 1: x1 > 4
axs[0].axvspan(0, 4, color=colors_il[0], alpha=0.15)
axs[0].axvspan(4, 10, color=colors_il[1], alpha=0.15)
axs[0].axvline(4, color="black", linewidth=2)
for k, x in enumerate([2, 7]):
    axs[0].text(x, 9.2, f"fulla {k + 1}", ha="center", fontsize=11)
axs[0].set_title("profunditat 1: un tall (x1 > 4) -> 2 fulles")

# profunditat 2: a l'esquerra x2 > 6, a la dreta x2 > 3
rect_il = [(0, 0, 4, 6), (0, 6, 4, 4), (4, 0, 6, 3), (4, 3, 6, 7)]
for k, (x0, y0, ample, alt) in enumerate(rect_il):
    axs[1].add_patch(plt.Rectangle((x0, y0), ample, alt, color=colors_il[k], alpha=0.15))
    axs[1].text(x0 + ample / 2, y0 + alt / 2, f"fulla {k + 1}", ha="center", fontsize=11)
axs[1].axvline(4, color="black", linewidth=2)
axs[1].plot([0, 4], [6, 6], color="black", linewidth=1.5, linestyle="--")
axs[1].plot([4, 10], [3, 3], color="black", linewidth=1.5, linestyle="--")
axs[1].set_title("profunditat 2: cada meitat es torna a partir -> 4 fulles")

for ax in axs:
    ax.scatter(X_il[:, 0], X_il[:, 1], color="tab:gray", edgecolors="k", s=15)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("x1")
axs[0].set_ylabel("x2")
fig.suptitle("Talls posats a mà sobre punts inventats: cada fulla és un rectangle")
plt.tight_layout()
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 5 — Soroll", [
    M(r"""
Abans de començar, la idea en un dibuix: què vol dir «més soroll» a les dades. Dos núvols
inventats amb el mateix centre i la mateixa mida de mostra; només canvia com
d'escampats estan. Com més soroll, més punts d'una classe cauen enmig de l'altra. Què
fa això a cada model és el que ha de dir la vostra taula.
"""),
    C(r"""
fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), sharex=True, sharey=True)
for ax, escampat_il in zip(axs, [0.3, 0.8, 1.5]):
    rng = np.random.default_rng(0)                      # mateixa llavor: només canvia el soroll
    X_il = np.vstack([rng.normal([-1, 0], escampat_il, (100, 2)),
                      rng.normal([1, 0], escampat_il, (100, 2))])
    y_il = np.array([0] * 100 + [1] * 100)
    ax.scatter(X_il[:, 0], X_il[:, 1], c=y_il, cmap="coolwarm", edgecolors="k", s=15)
    ax.set_title(f"soroll (desviació) = {escampat_il}")
    ax.grid(alpha=0.3)
fig.suptitle("Dades inventades: el mateix problema amb cada cop més soroll")
plt.tight_layout()
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 6 — Fabricar un problema a mida", [
    M(r"""
Abans de començar, la idea en un dibuix: per què cal repetir amb diversos
`random_state`. Cada punt és la diferència d'exactitud *model A − model B* en una
partició diferent. Els números són **inventats** i els models no tenen nom a propòsit. A
l'esquerra, la diferència canvia de signe segons la partició: no se'n pot concloure
res. A la dreta, totes les particions donen el mateix signe: aquí sí.
"""),
    C(r"""
rng = np.random.default_rng(8)
llavors_il = np.arange(8)
dif_dubtosa_il = rng.normal(0.0, 0.02, 8)             # inventat
dif_clara_il = rng.normal(0.06, 0.015, 8)               # inventat

fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
for ax, dif_il, titol in [(axs[0], dif_dubtosa_il, "canvia de signe: no és una diferència"),
                          (axs[1], dif_clara_il, "sempre del mateix costat: sí que ho és")]:
    colors_il = ["tab:green" if d > 0 else "tab:red" for d in dif_il]
    ax.bar(llavors_il, dif_il, color=colors_il)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks(llavors_il)
    ax.set_xlabel("random_state del train_test_split")
    ax.set_title(titol)
    ax.grid(alpha=0.3, axis="y")
axs[0].set_ylabel("exactitud A − exactitud B")
fig.suptitle("Números inventats: la mateixa comparació repetida amb vuit particions")
plt.tight_layout()
plt.show()
"""),
]))

INSERCIONS.append(("## Exercici 7 — Tancament", [
    M(r"""
Abans de començar, la idea en un dibuix: com es decideix si una aposta és un encert.
Exactituds **inventades** de tres models inventats en dos conjunts inventats. La línia
és el llindar de 0,85; el triangle amunt és una aposta «bé» i l'avall, «malament». Verd
si l'aposta i el costat de la línia coincideixen, vermell si no.
"""),
    C(r"""
LLINDAR_il = 0.85
casos_il = [("conjunt X", "model P", "bé", 0.97), ("conjunt X", "model Q", "malament", 0.91),
            ("conjunt X", "model R", "bé", 0.88), ("conjunt Y", "model P", "malament", 0.62),
            ("conjunt Y", "model Q", "bé", 0.79), ("conjunt Y", "model R", "malament", 0.71)]

fig, ax = plt.subplots(figsize=(10, 4.2))
for k, (conjunt, model_nom, aposta, prec) in enumerate(casos_il):
    encert = (aposta == "bé") == (prec >= LLINDAR_il)
    ax.scatter(k, prec, marker="^" if aposta == "bé" else "v", s=220,
               color="tab:green" if encert else "tab:red", edgecolors="k", zorder=3)
    ax.annotate("encert" if encert else "error", (k, prec), textcoords="offset points",
                xytext=(0, 14), ha="center")
ax.axhline(LLINDAR_il, color="black", linestyle="--", label="llindar 0,85")
ax.set_xticks(range(len(casos_il)), [f"{c}\n{m}" for c, m, _, _ in casos_il])
ax.set_ylim(0.5, 1.05)
ax.set_ylabel("exactitud real")
ax.set_title("Números inventats: aposta (triangle) contra exactitud real (alçada)")
ax.legend(loc="lower left")
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.show()
"""),
]))


def text(c):
    return "".join(c["source"])


def main():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    cells = [c for c in nb["cells"] if c.get("metadata", {}).get("grafic") != MARCA]
    for ancora, noves in INSERCIONS:
        idx = [i for i, c in enumerate(cells) if ancora in text(c)]
        if len(idx) != 1:
            raise SystemExit(f"Ancoratge no trobat o repetit ({len(idx)}): {ancora!r}")
        cells[idx[0] + 1:idx[0] + 1] = noves
    nb["cells"] = cells
    io.open(RUTA, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    print(f"{RUTA}: {len(cells)} cel.les ({sum(len(n) for _, n in INSERCIONS)} afegides)")


if __name__ == "__main__":
    main()
