# -*- coding: utf-8 -*-
"""Afegeix els grafics al quadern ML_03_boscos (que no te generador).

Llegeix el .ipynb, treu les cel.les que ja hi havia afegit aquest script (marcades
amb `metadata.grafic_afegit`), hi torna a inserir les noves despres de la cel.la
ancora corresponent i el desa. Es pot tornar a executar sense duplicar res.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_ML_03.py
"""
import io
import json
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code

RUTA = "Machine Learning/01_teoria/ML_03_boscos.ipynb"
MARCA = "grafic_afegit"
FRASE_PRACTICA = ("Abans de cada exercici hi ha un dibuix amb **dades inventades** que "
                  "ensenya la idea o com es mesura el que es demana; els números de debò "
                  "els heu de treure vosaltres.")


def marca(c):
    c["metadata"][MARCA] = True
    return c


INSERCIONS = []

# --- teoria 1: tres mostres bootstrap, fila a fila
INSERCIONS.append(("\\\nSurt gairebé exactament $1/e", [
    md(r"""
Vegem-ho fila a fila. Tres mostres bootstrap de **20 files**: cada barra diu quantes
vegades ha sortit aquella fila a la mostra. Les creus vermelles són les files que aquell
arbre no veurà mai; fixeu-vos que **no són les mateixes** a cada mostra.
"""),
    code(r"""
rng_boot = np.random.default_rng(5)
n_fil = 20

fig, eixos = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True, sharey=True)
for k, ax in enumerate(eixos):
    mostra_k = rng_boot.integers(0, n_fil, size=n_fil)
    vegades = np.bincount(mostra_k, minlength=n_fil)
    fora_k = np.flatnonzero(vegades == 0)
    ax.bar(np.arange(n_fil), vegades, color="tab:blue")
    ax.scatter(fora_k, np.zeros(len(fora_k)) + 0.15, marker="x", color="tab:red", s=60,
               zorder=3, label="no ha sortit")
    ax.set_ylabel("vegades")
    ax.set_title(f"Mostra bootstrap {k + 1}: {len(fora_k)} de {n_fil} files fora "
                 f"({len(fora_k) / n_fil:.0%})", fontsize=10)
    ax.grid(alpha=0.3, axis="y")
eixos[0].legend(loc="upper right")
eixos[-1].set_xticks(range(n_fil))
eixos[-1].set_xlabel("fila de l'entrenament")
plt.tight_layout()
plt.show()
"""),
]))

# --- teoria 2: fronteres d'arbres individuals i la del bosc
INSERCIONS.append(("Amb només dues de les quatre columnes disponibles", [
    md(r"""
### Com es veu al pla

Amb dades inventades de dues classes (les «mitges llunes» de scikit-learn, amb soroll),
entrenem quatre arbres sense límit de profunditat, cadascun amb la seva mostra bootstrap.
Cada un dibuixa una frontera **plena de racons**: s'ha cregut el soroll de les seves files.
A sota, el bosc de 100 arbres: a l'esquerra el vot de la majoria, a la dreta **la fracció
d'arbres** que voten taronja a cada punt del pla. Els racons de cada arbre van a llocs
diferents, i en fer la mitjana s'esborren.
"""),
    code(r"""
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X_ll, y_ll = make_moons(n_samples=300, noise=0.3, random_state=0)
gx, gy = np.meshgrid(np.linspace(-2, 3, 300), np.linspace(-1.6, 2.1, 250))
punts_graella = np.c_[gx.ravel(), gy.ravel()]
cmap_dur = ListedColormap(["tab:blue", "tab:orange"])
cmap_suau = LinearSegmentedColormap.from_list("blau_taronja", ["tab:blue", "white", "tab:orange"])
rng_ll = np.random.default_rng(1)


def pinta_punts(ax):
    ax.scatter(X_ll[:, 0], X_ll[:, 1], c=y_ll, cmap=cmap_dur, edgecolor="k", s=14, linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])


fig, eixos = plt.subplots(2, 3, figsize=(13, 8))
for k, ax in enumerate(eixos.ravel()[:4]):
    idx_b = rng_ll.integers(0, len(X_ll), size=len(X_ll))
    a_b = DecisionTreeClassifier(random_state=k).fit(X_ll[idx_b], y_ll[idx_b])
    ax.contourf(gx, gy, a_b.predict(punts_graella).reshape(gx.shape), levels=[-0.5, 0.5, 1.5],
                cmap=cmap_dur, alpha=0.3)
    pinta_punts(ax)
    ax.set_title(f"Arbre {k + 1} (la seva mostra bootstrap)")

bosc_ll = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_ll, y_ll)
vots_taronja = bosc_ll.predict_proba(punts_graella)[:, 1].reshape(gx.shape)

ax = eixos[1, 1]
ax.contourf(gx, gy, (vots_taronja > 0.5).astype(int), levels=[-0.5, 0.5, 1.5], cmap=cmap_dur, alpha=0.3)
pinta_punts(ax)
ax.set_title("El bosc de 100: vot de la majoria")

ax = eixos[1, 2]
mapa = ax.contourf(gx, gy, vots_taronja, levels=np.linspace(0, 1, 11), cmap=cmap_suau)
pinta_punts(ax)
ax.set_title("El bosc de 100: fracció de vots taronja")
fig.colorbar(mapa, ax=ax, fraction=0.046)
fig.suptitle("Dades inventades: cada arbre s'equivoca a la seva manera; la mitjana és més suau")
plt.tight_layout()
plt.show()
"""),
]))

# --- teoria 3: error segons el nombre d'arbres, al problema dificil
INSERCIONS.append(("Amb 20 columnes, soroll i relacions", [
    md(r"""
Quants arbres calen perquè el bosc guanyi? Dibuixem l'**error** d'examen (1 − precisió)
en aquest mateix problema difícil, afegint arbres d'un en un al principi i de molts en
molts després. La línia grisa és l'arbre sol.
"""),
    code(r"""
n_arbres_corba = [1, 2, 3, 5, 8, 12, 20, 30, 50, 75, 100, 150, 200]
error_corba = []
for n in n_arbres_corba:
    b = RandomForestClassifier(n_estimators=n, random_state=42, n_jobs=-1)
    b.fit(Xc_entrena, yc_entrena)
    error_corba.append(1 - b.score(Xc_examen, yc_examen))

plt.figure(figsize=(8, 5))
plt.plot(n_arbres_corba, error_corba, marker="o", color="tab:blue", label="bosc aleatori")
plt.axhline(1 - precisio_arbre_dificil, color="gray", linestyle="--", label="un sol arbre")
plt.xscale("log")
plt.xticks(n_arbres_corba, [str(n) for n in n_arbres_corba])
plt.xlabel("Nombre d'arbres (escala logarítmica)")
plt.ylabel("Error a l'examen")
plt.title("make_classification: l'error baixa de pressa i després s'aplana")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""),
    md(r"""
Amb un o dos arbres el bosc és fins i tot pitjor que l'arbre sol (cada arbre veu menys
files i menys columnes). Amb tres ja l'ha passat, amb una dotzena ja és a prop del mínim, i
a partir d'aquí cada arbre de més aporta molt poc: la corba s'aplana i només balla. Afegir arbres **no
sobreajusta**, però tampoc no millora indefinidament.
"""),
]))

# --- teoria 4: importancies quan sabem la resposta
INSERCIONS.append(("El resultat no hauria de sorprendre't: les columnes del pètal", [
    md(r"""
Per saber si les importàncies diuen alguna cosa sensata, cal un problema on **sapiguem la
resposta**. `make_classification` amb `shuffle=False` posa les columnes en ordre: primer
les 5 informatives, després les 5 redundants (combinacions de les informatives) i al final
les 10 de soroll pur. Entrenem-hi un bosc i pintem cada barra segons el tipus de columna.
"""),
    code(r"""
Xi, yi = make_classification(
    n_samples=2_000, n_features=20, n_informative=5, n_redundant=5,
    n_clusters_per_class=2, flip_y=0.05, shuffle=False, random_state=42,
)
from matplotlib.patches import Patch

bosc_imp = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1).fit(Xi, yi)

tipus_col = ["informativa"] * 5 + ["redundant"] * 5 + ["soroll"] * 10
color_tipus = {"informativa": "tab:green", "redundant": "tab:orange", "soroll": "gray"}

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.bar(range(20), bosc_imp.feature_importances_, color=[color_tipus[t] for t in tipus_col])
ax.set_xticks(range(20), [f"c{i}" for i in range(20)])
ax.set_xlabel("columna")
ax.set_ylabel("Importància")
ax.set_title("Dades inventades amb la resposta coneguda: importàncies del bosc")
ax.legend(handles=[Patch(color=c, label=t) for t, c in color_tipus.items()])
ax.grid(alpha=0.3, axis="y")
plt.show()
"""),
    md(r"""
Les columnes de soroll queden totes a baix, i les informatives i les redundants a dalt,
barrejades: el bosc no distingeix una columna «original» d'una que n'és una combinació,
perquè totes dues porten la mateixa informació. La importància diu **què ha fet servir**
el bosc, no **què causa** l'etiqueta.
"""),
]))

# --- exercici 7.1: com es mesura "deixa de valer la pena"
INSERCIONS.append(("### 7.1 Quants arbres calen?", [
    md(r"""
Abans de començar, la idea en un dibuix: una corba de precisió **inventada** i una manera
de mesurar «deixa de valer la pena». La banda grisa és ±1 punt al voltant de la precisió
amb el nombre d'arbres més gran; el punt vermell és el primer nombre d'arbres a partir
del qual la corba ja no en surt. Amb les vostres dades la corba pot tenir una forma ben
diferent (fins i tot plana).
"""),
    code(r"""
n_il = np.array([1, 5, 10, 25, 50, 100, 200])
prec_il = np.array([0.780, 0.845, 0.872, 0.884, 0.893, 0.889, 0.891])     # inventada
final_il = prec_il[-1]
dins_il = np.abs(prec_il - final_il) <= 0.01
# primer index a partir del qual TOTS els seguents son dins de la banda
primer_il = next(i for i in range(len(n_il)) if dins_il[i:].all())

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axhspan(final_il - 0.01, final_il + 0.01, color="gray", alpha=0.2, label="±1 punt del valor final")
ax.plot(n_il, prec_il, marker="o", color="tab:blue", label="precisió (inventada)")
ax.scatter([n_il[primer_il]], [prec_il[primer_il]], s=150, facecolor="none",
           edgecolor="tab:red", linewidth=2, zorder=3,
           label=f"a partir de {n_il[primer_il]} arbres ja no en surt")
ax.set_xscale("log")
ax.set_xticks(n_il, [str(n) for n in n_il])
ax.set_xlabel("n_estimators (escala logarítmica)")
ax.set_ylabel("Precisió a l'examen")
ax.set_title("Dades inventades: on s'aplana la corba")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
plt.show()
"""),
]))

# --- exercici 7.2: una sola particio es mou
INSERCIONS.append(("### 7.2 Arbre contra bosc amb Wine", [
    md(r"""
Abans de començar, la idea en un dibuix: abans de dir qui guanya, mireu **quant es mou la
precisió només canviant la partició**. Un sol arbre sobre dades inventades, avaluat amb 40
`random_state` diferents de `train_test_split`. La línia vermella és el que hauríeu vist
amb una sola partició; l'amplada de l'histograma és el soroll que té qualsevol
comparació feta així.
"""),
    code(r"""
from sklearn.datasets import make_moons

X_il, y_il = make_moons(n_samples=180, noise=0.35, random_state=3)
prec_parts_il = []
for llavor in range(40):
    Xa, Xb, ya, yb = train_test_split(X_il, y_il, test_size=0.3, random_state=llavor)
    prec_parts_il.append(DecisionTreeClassifier(random_state=0).fit(Xa, ya).score(Xb, yb))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(prec_parts_il, bins=10, color="tab:blue", edgecolor="white")
ax.axvline(prec_parts_il[0], color="tab:red", linestyle="--", linewidth=2,
           label=f"una sola partició (random_state=0): {prec_parts_il[0]:.1%}")
ax.set_xlabel("Precisió a l'examen")
ax.set_ylabel("Nombre de particions")
ax.set_title(f"Dades inventades: el mateix model, 40 particions "
             f"(de {min(prec_parts_il):.0%} a {max(prec_parts_il):.0%})")
ax.legend()
ax.grid(alpha=0.3, axis="y")
plt.show()
"""),
]))

# --- exercici 7.3: mesurar temps
INSERCIONS.append(("### 7.3 El preu de tants arbres", [
    md(r"""
Abans de començar, la idea en un dibuix: com es mesura un temps amb `time.time()`. No hi
ha cap bosc: cronometrem `np.sort` amb vectors de mides diferents, **cinc vegades cada
una**. Els punts d'una mateixa mida no surten iguals; per això convé repetir la mesura i
quedar-se amb la mitjana (o la mediana).
"""),
    code(r"""
import time

mides_il = [100_000, 200_000, 400_000, 800_000, 1_600_000]
rng_t = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(8, 4.5))
for mida in mides_il:
    v = rng_t.random(mida)
    temps = []
    for _ in range(5):
        inici = time.time()
        np.sort(v)
        temps.append(time.time() - inici)
    ax.scatter([mida] * 5, temps, color="tab:blue", alpha=0.5)
    ax.scatter([mida], [np.median(temps)], color="tab:red", marker="_", s=400, linewidth=2)
ax.scatter([], [], color="tab:red", marker="_", s=200, label="mediana de les 5 mesures")
ax.set_xlabel("mida del vector")
ax.set_ylabel("segons")
ax.set_title("Cronometrar amb time.time(): cada mesura surt una mica diferent")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.show()
"""),
]))

# --- exercici 7.4: com es veu "copiar el vot"
INSERCIONS.append(("### 7.4 Trenca la independència", [
    md(r"""
Abans de començar, la idea en un dibuix: els vots de 12 classificadors (files) en 40
casos (columnes), verd si encerta i vermell si falla. A l'esquerra voten cadascun pel seu
compte; a la dreta, cada un copia el vot del primer el 80 % de les vegades. Fixeu-vos en
les **columnes**: a la dreta els errors s'apilen al mateix cas. Quant val la majoria en
cada cas ho heu de calcular vosaltres.
"""),
    code(r"""
rng_v = np.random.default_rng(2)
n_cl, n_casos = 12, 40
indep_il = rng_v.random((n_cl, n_casos)) < 0.6

primer_il = rng_v.random(n_casos) < 0.6
copia_il = rng_v.random((n_cl, n_casos)) < 0.8
propi_il = rng_v.random((n_cl, n_casos)) < 0.6
corr_il = np.where(copia_il, primer_il, propi_il)
corr_il[0] = primer_il

from matplotlib.colors import ListedColormap

cmap_vots = ListedColormap(["tab:red", "tab:green"])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 3.8), sharey=True)
for ax, vots_il, titol in [(ax1, indep_il, "Independents"),
                           (ax2, corr_il, "Copiant el primer el 80 % de les vegades")]:
    ax.imshow(vots_il, cmap=cmap_vots, aspect="auto", vmin=0, vmax=1)
    ax.set_title(titol)
    ax.set_xlabel("cas")
ax1.set_ylabel("classificador")
fig.suptitle("Dades inventades: verd = encert, vermell = error")
plt.tight_layout()
plt.show()
"""),
]))


def main():
    nb = json.load(io.open(RUTA, encoding="utf-8"))
    cells = [c for c in nb["cells"] if not c["metadata"].get(MARCA)]

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
