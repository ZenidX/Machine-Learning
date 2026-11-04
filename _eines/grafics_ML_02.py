# -*- coding: utf-8 -*-
"""Afegeix els grafics al quadern ML_02_arbres (que no te generador).

Llegeix el .ipynb, treu les cel.les que ja hi havia afegit aquest script (marcades
amb `metadata.grafic_afegit`), hi torna a inserir les noves despres de la cel.la
ancora corresponent i el desa. Es pot tornar a executar sense duplicar res.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_ML_02.py
"""
import io
import json
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code

RUTA = "Machine Learning/01_teoria/ML_02_arbres.ipynb"
MARCA = "grafic_afegit"
FRASE_PRACTICA = ("Abans de cada exercici hi ha un dibuix amb **dades inventades** que "
                  "ensenya la idea; els números de debò els heu de treure vosaltres.")


def marca(c):
    c["metadata"][MARCA] = True
    return c


# ------------------------------------------------------------------ cel.les noves
# Cada entrada: (inici del text de la cel.la ancora, [cel.les a posar DESPRES])
INSERCIONS = []

# --- teoria 1: corbes de Gini i entropia segons la proporcio
INSERCIONS.append(("Els números surten exactament com s'esperava", [
    md(r"""
### Les dues mesures en un dibuix

Amb **dues** classes, tot el grup es resumeix en un sol número: la proporció $p$ de la
primera classe (la de l'altra és $1-p$). Així podem dibuixar Gini i entropia per a totes
les barreges possibles, de la puresa total ($p=0$ o $p=1$) a l'empat ($p=0{,}5$).
L'entropia la calculem aquí amb `scipy`, perquè la vostra la fareu a l'exercici 1.
"""),
    code(r"""
from scipy.stats import entropy as entropia_scipy

p_corba = np.linspace(0, 1, 201)
gini_corba = 1 - p_corba ** 2 - (1 - p_corba) ** 2
entropia_corba = np.array([entropia_scipy([p, 1 - p], base=2) for p in p_corba])

plt.figure(figsize=(8, 5))
plt.plot(p_corba, gini_corba, color="tab:orange", linewidth=2, label="Gini  $1 - p^2 - (1-p)^2$")
plt.plot(p_corba, entropia_corba, color="tab:blue", linewidth=2, label="Entropia (bits)")
plt.scatter([0.5, 0.5], [0.5, 1.0], color="tab:red", zorder=3)
plt.annotate("empat 50/50: Gini = 0,5", (0.5, 0.5), xytext=(0.58, 0.32),
             arrowprops=dict(arrowstyle="->", color="gray"))
plt.annotate("empat 50/50: entropia = 1 bit", (0.5, 1.0), xytext=(0.6, 0.88),
             arrowprops=dict(arrowstyle="->", color="gray"))
plt.xlabel("p (proporció de la primera classe dins del grup)")
plt.ylabel("Impuresa")
plt.title("Impuresa d'un grup de dues classes segons la barreja")
plt.legend(loc="upper left")
plt.grid(alpha=0.3)
plt.show()
"""),
    md(r"""
Les dues corbes valen 0 als extrems (grup pur) i tenen el màxim al mig (barreja
equilibrada). Tenen escales diferents, però la **forma** és la mateixa: per això, a l'hora
de comparar talls, gairebé sempre ordenen els candidats igual.
"""),
]))

# --- teoria 2: escombrar el llindar d'una columna (dades inventades)
INSERCIONS.append(("## 3. Com tria la màquina el tall", [
    md(r"""
Abans d'implementar-ho, vegem què vol dir **escombrar un llindar** amb vint punts
inventats d'una sola columna i dues classes. Per a cada llindar candidat calculem la
impuresa de cada costat i la ponderada; el tall bo és on la ponderada toca fons.
"""),
    code(r"""
rng = np.random.default_rng(4)
x_inv = np.round(np.concatenate([rng.normal(3, 1.0, 10), rng.normal(6, 1.0, 10)]), 2)
y_inv = np.array(["A"] * 10 + ["B"] * 10)

valors_inv = np.sort(np.unique(x_inv))
llindars_inv = (valors_inv[:-1] + valors_inv[1:]) / 2
g_esq_inv, g_dre_inv, g_pond_inv = [], [], []
for t in llindars_inv:
    esq, dre = y_inv[x_inv <= t], y_inv[x_inv > t]
    g_esq_inv.append(gini(esq))
    g_dre_inv.append(gini(dre))
    g_pond_inv.append(len(esq) / 20 * gini(esq) + len(dre) / 20 * gini(dre))
millor_inv = llindars_inv[int(np.argmin(g_pond_inv))]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True,
                               gridspec_kw={"height_ratios": [1, 2.2]})
for classe, color in [("A", "tab:blue"), ("B", "tab:orange")]:
    ax1.scatter(x_inv[y_inv == classe], np.zeros(10), color=color, edgecolor="k",
                s=60, label=f"classe {classe}", zorder=3)
ax1.axvline(millor_inv, color="tab:red", linestyle="--", label="millor llindar")
ax1.set_yticks([])
ax1.set_title("Vint punts inventats d'una sola columna")
ax1.legend(loc="upper left", ncol=3)
ax1.grid(alpha=0.3)

ax2.plot(llindars_inv, g_esq_inv, color="tab:blue", alpha=0.5, label="Gini de l'esquerra")
ax2.plot(llindars_inv, g_dre_inv, color="tab:orange", alpha=0.5, label="Gini de la dreta")
ax2.plot(llindars_inv, g_pond_inv, color="tab:red", linewidth=2.5, marker="o",
         markersize=4, label="Gini ponderat dels dos fills")
ax2.axhline(gini(y_inv), color="gray", linestyle=":", label="Gini del pare (sense tallar)")
ax2.axvline(millor_inv, color="tab:red", linestyle="--")
ax2.set_xlabel("llindar de tall")
ax2.set_ylabel("Impuresa de Gini")
ax2.set_title("Escombrant el llindar: el guany és la distància fins a la línia grisa")
ax2.set_ylim(-0.02, 0.68)
ax2.legend(loc="upper center", ncol=2, fontsize=9)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),
    md(r"""
Als extrems, un dels dos fills té quatre punts i l'altre és gairebé tot el grup: la
ponderada quasi no baixa. Al mig, on les dues classes se separen, els dos fills són
gairebé purs i la ponderada s'enfonsa. `millor_tall` fa exactament això, per a **totes**
les columnes alhora, i es queda amb el mínim de tots.
"""),
]))

# --- teoria 3: l'arbre com a talls rectangulars del pla, per profunditat
INSERCIONS.append(("Amb `max_depth=1` l'arbre encerta un 66,7 %", [
    md(r"""
### El sobreajust al pla

Un arbre només fa preguntes del tipus «columna ≤ llindar», així que **parteix el pla en
rectangles**, i cada rectangle és una fulla. Ho veiem amb només dues columnes, les del
sèpal (on les espècies es barregen més), i quatre profunditats.
"""),
    code(r"""
from matplotlib.colors import ListedColormap

cols_pla = ["sepal_llarg", "sepal_ample"]
especies_pla = np.array(["setosa", "versicolor", "virginica"])
colors_pla = ["tab:blue", "tab:orange", "tab:green"]
xx, yy = np.meshgrid(np.linspace(4, 8.2, 400), np.linspace(1.8, 4.6, 300))
graella = pd.DataFrame({cols_pla[0]: xx.ravel(), cols_pla[1]: yy.ravel()})

fig, eixos = plt.subplots(2, 2, figsize=(11, 9), sharex=True, sharey=True)
for ax, p in zip(eixos.ravel(), [1, 2, 3, 8]):
    a = DecisionTreeClassifier(max_depth=p, random_state=42)
    a.fit(X_entrena[cols_pla], y_entrena)
    zona = np.searchsorted(especies_pla, a.predict(graella)).reshape(xx.shape)
    ax.contourf(xx, yy, zona, levels=[-0.5, 0.5, 1.5, 2.5],
                cmap=ListedColormap(colors_pla), alpha=0.25)
    for esp, color in zip(especies_pla, colors_pla):
        m = (y_entrena == esp).to_numpy()
        ax.scatter(X_entrena[cols_pla[0]][m], X_entrena[cols_pla[1]][m], color=color,
                   edgecolor="k", s=25, label=esp)
    ax.set_title(f"max_depth={p}: {a.get_n_leaves()} fulles · entrena "
                 f"{a.score(X_entrena[cols_pla], y_entrena):.0%} · examen "
                 f"{a.score(X_examen[cols_pla], y_examen):.0%}", fontsize=10)
    ax.grid(alpha=0.3)
for ax in eixos[1]:
    ax.set_xlabel("sepal_llarg (cm)")
for ax in eixos[:, 0]:
    ax.set_ylabel("sepal_ample (cm)")
eixos[0, 0].legend(loc="upper right", fontsize=9)
fig.suptitle("Cada tall afegeix rectangles; a profunditat 8 apareixen illes per a una o dues flors")
plt.tight_layout()
plt.show()
"""),
    md(r"""
A profunditat 1 hi ha una sola frontera recta. A 2 i 3 apareixen rectangles que segueixen
les zones de cada espècie. A 8, l'arbre dibuixa **illes** petites al voltant de flors
concretes d'entrenament: per això encerta més a entrenament i no més a l'examen. Una flor
nova que caigui a prop d'una d'aquestes illes hereta la decisió d'una sola flor, no la
d'una zona.
"""),
]))

# --- exercici 1: l'entropia com a pila de contribucions
INSERCIONS.append(("### Exercici 1 — Implementa l'entropia", [
    md(r"""
Abans de començar, la idea en un dibuix: a la fórmula, **cada classe aporta un tros**
$-p_i\log_2 p_i$, i l'entropia del grup és la pila de tots els trossos. Quatre grups
inventats (no són els de la comprovació); els trossos els calcula `scipy.special.entr`,
que la fórmula l'heu d'escriure vosaltres.
"""),
    code(r"""
from scipy.special import entr      # entr(p) = -p * ln(p), element a element

grups_il = {
    "80 / 20": [0.8, 0.2],
    "60 / 30 / 10": [0.6, 0.3, 0.1],
    "45 / 45 / 10": [0.45, 0.45, 0.1],
    "40 / 35 / 25": [0.4, 0.35, 0.25],
}
colors_il = ["tab:blue", "tab:orange", "tab:green"]

fig, ax = plt.subplots(figsize=(8, 5))
for j, (nom, props) in enumerate(grups_il.items()):
    trossos = entr(np.array(props)) / np.log(2)          # passem de nats a bits
    base = 0.0
    for k, tros in enumerate(trossos):
        ax.bar(j, tros, bottom=base, color=colors_il[k], edgecolor="white",
               label=f"classe {k + 1}" if j == 1 else None)
        base += tros
    ax.text(j, base + 0.03, f"{base:.2f} bits", ha="center")
ax.set_xticks(range(len(grups_il)), [f"grup {g}" for g in grups_il])
ax.set_ylabel("$-p_i \\log_2 p_i$ apilat (bits)")
ax.set_title("Dades inventades: l'entropia és la suma de l'aportació de cada classe")
ax.legend()
ax.grid(alpha=0.3, axis="y")
plt.show()
"""),
]))

# --- exercici 2: el segon nivell es busca per separat a cada meitat
INSERCIONS.append(("### Exercici 2 — Construïu a mà un arbre de profunditat 2", [
    md(r"""
Abans de començar, la idea en un dibuix: punts inventats de dues classes en un pla. El
primer tall travessa **tot** el pla. Els del segon nivell es busquen **per separat** a cada
meitat, i per això cada un pot fer servir una columna diferent i només ocupa la seva
meitat. Els talls d'aquest dibuix estan posats a mà; els d'Iris els heu de trobar vosaltres.
"""),
    code(r"""
rng = np.random.default_rng(11)
P_il = rng.uniform(0, 10, size=(160, 2))
a_il, b_il = P_il[:, 0], P_il[:, 1]
y_il = np.where(a_il <= 4, b_il > 5, a_il <= 7).astype(int)     # regla amagada
soroll_il = rng.random(160) < 0.05
y_il[soroll_il] = 1 - y_il[soroll_il]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
for ax in (ax1, ax2):
    for k, color in [(0, "tab:blue"), (1, "tab:orange")]:
        ax.scatter(a_il[y_il == k], b_il[y_il == k], color=color, edgecolor="k", s=25,
                   label=f"classe {k}")
    ax.axvline(4, color="tab:red", linewidth=2.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("columna a")
    ax.grid(alpha=0.3)
ax1.set_ylabel("columna b")
ax1.set_title("Nivell 1: un tall per a tot el pla (a ≤ 4)")
ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
ax2.plot([0, 4], [5, 5], color="tab:green", linewidth=2.5, label="tall de l'esquerra (b ≤ 5)")
ax2.plot([7, 7], [0, 10], color="tab:purple", linewidth=2.5, label="tall de la dreta (a ≤ 7)")
ax2.set_title("Nivell 2: un tall nou dins de cada meitat")
ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=9)
plt.tight_layout()
plt.show()
"""),
]))

# --- exercici 3: millor_tall mira totes les columnes, cadascuna en les seves unitats
INSERCIONS.append(("### Exercici 3 — Un altre dataset: Wine", [
    md(r"""
Abans de començar, la idea en un dibuix: tres columnes inventades, cadascuna amb unitats
molt diferents (com passa a Wine). `millor_tall` dibuixa la corba de guany de **cada**
columna en les seves unitats, en marca el màxim, i es queda amb el màxim dels màxims. Les
escales diferents no l'afecten: només compara guanys.
"""),
    code(r"""
rng = np.random.default_rng(21)
n_il = 120
classe_il = rng.integers(0, 3, n_il)
cols_il = {
    "acidesa (0-1)": np.clip(0.3 + 0.12 * classe_il + rng.normal(0, 0.12, n_il), 0, 1),
    "color (0-100)": 20 + 25 * classe_il + rng.normal(0, 6, n_il),
    "pes (0-2000 g)": rng.uniform(0, 2000, n_il),          # soroll pur
}

fig, eixos = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
millors_il = {}
for ax, (nom, valors) in zip(eixos, cols_il.items()):
    v = np.sort(np.unique(valors))
    ts = (v[:-1] + v[1:]) / 2
    g = [gini(classe_il) - gini_ponderat(classe_il[valors <= t], classe_il[valors > t])
         for t in ts]
    k = int(np.argmax(g))
    millors_il[nom] = g[k]
    ax.plot(ts, g, color="tab:blue")
    ax.scatter([ts[k]], [g[k]], color="tab:red", zorder=3, s=50)
    ax.set_title(f"{nom}\nmillor guany {g[k]:.3f}", fontsize=10)
    ax.set_xlabel("llindar (unitats de la columna)")
    ax.grid(alpha=0.3)
eixos[0].set_ylabel("Guany de Gini")
guanyadora_il = max(millors_il, key=millors_il.get)
fig.suptitle(f"Dades inventades: guanya «{guanyadora_il}», el màxim dels màxims")
plt.tight_layout()
plt.show()
"""),
]))

# --- exercici 4: argmax dona una posicio, no un max_depth
INSERCIONS.append(("### Exercici 4 — Trobeu la profunditat òptima", [
    md(r"""
Abans de començar, la idea en un dibuix: una corba de precisió **inventada**. `np.argmax`
retorna la **posició** del màxim dins de la llista, i les posicions comencen a 0; el
`max_depth` corresponent l'heu d'anar a buscar a la mateixa posició de `profunditats`.
"""),
    code(r"""
prof_il = list(range(1, 11))
prec_il = [0.62, 0.78, 0.85, 0.88, 0.91, 0.90, 0.89, 0.88, 0.88, 0.87]   # inventada
pos_il = int(np.argmax(prec_il))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(prof_il, prec_il, marker="o", color="tab:orange", label="examen (inventat)")
ax.scatter([prof_il[pos_il]], [prec_il[pos_il]], s=160, facecolor="none",
           edgecolor="tab:red", linewidth=2, zorder=3)
ax.annotate(f"np.argmax → posició {pos_il}\nprofunditats[{pos_il}] → max_depth = {prof_il[pos_il]}",
            (prof_il[pos_il], prec_il[pos_il]), xytext=(6.3, 0.70),
            arrowprops=dict(arrowstyle="->", color="tab:red"))
ax.set_xticks(prof_il)
ax.set_xlabel("max_depth")
ax.set_ylabel("Precisió")
ax.set_title("Dades inventades: la posició del màxim no és el max_depth")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
plt.show()
"""),
]))


# ------------------------------------------------------------------ aplicar
def main():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    cells = [c for c in nb["cells"] if not c["metadata"].get(MARCA)]

    # petit ajust a la introduccio de la practica
    for c in cells:
        text = "".join(c["source"])
        if text.startswith("## 7. Pràctica"):
            base = text.replace(FRASE_PRACTICA, "").rstrip("\n")
            c["source"] = md(base + "\n\n" + FRASE_PRACTICA)["source"]

    for inici, noves in INSERCIONS:
        idx = [i for i, c in enumerate(cells) if "".join(c["source"]).startswith(inici)]
        if len(idx) != 1:
            raise SystemExit(f"ancora no trobada o repetida: {inici!r} -> {idx}")
        cells[idx[0] + 1:idx[0] + 1] = [marca(c) for c in noves]

    nb["cells"] = cells
    io.open(RUTA, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
    print(RUTA, "cel.les:", len(cells), "afegides:",
          sum(1 for c in cells if c["metadata"].get(MARCA)))


if __name__ == "__main__":
    main()
