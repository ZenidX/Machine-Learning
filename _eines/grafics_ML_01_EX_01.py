# -*- coding: utf-8 -*-
"""Afegeix els grafics a ML_01_knn.ipynb i a EX_01_wine.ipynb.

Aquests dos quaderns no tenen generador propi: aquest script llegeix el .ipynb,
treu les cel.les que hi va posar en una passada anterior (les reconeix per
`metadata.grafic`) i hi torna a inserir les noves, ancorades al text de les
cel.les existents. Es pot tornar a executar tantes vegades com calgui.

- ML_01: grafics a la teoria (contribucio de cada columna a la distancia,
  Manhattan contra euclidiana, els k veins i el vot, frontera k=1 / k=15 / k=200,
  exactitud d'entrenament contra examen segons k, el parany de les escales) i un
  grafic il.lustratiu amb dades inventades abans de cada exercici.
- EX_01: un grafic il.lustratiu amb dades inventades abans de cada exercici.
  Ensenyen com es mesura el que es demana, mai el resultat amb Wine.

    CEIABD-IA/.venv/Scripts/python.exe _eines/grafics_ML_01_EX_01.py

Despres: executar amb nbconvert --inplace, buidar les sortides de les cel.les
d'exercici (ho fa aquest mateix script amb --neteja) i passar treu_widgets.py.
"""
import io
import json
import sys

sys.path.insert(0, "_eines")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from nbgen import md, code

ML01 = "Machine Learning/01_teoria/ML_01_knn.ipynb"
EX01 = "Machine Learning/02_practica/EX_01_wine.ipynb"


def g(cel, nom):
    cel["metadata"]["grafic"] = nom
    return cel


# =====================================================================  ML_01
ML01_INSERCIONS = []   # (text que identifica la cel.la ancora, [cel.les a posar DESPRES])

# --- 2. quant aporta cada columna a la distancia en 4D
ML01_INSERCIONS.append(("dist_4d = np.sqrt(np.sum(diferencies ** 2))", [
    g(md(r"""
La fórmula en un dibuix: cada barra és un sumand $(a_i - b_i)^2$. La distància al quadrat és
**la suma de les quatre barres**, i la distància és la seva arrel. Fixeu-vos quina columna
aporta més: és la que més pesa a l'hora de decidir qui és a prop de qui.
"""), "ml01_barres4d"),
    g(code(r"""
quadrats = diferencies ** 2

fig, ax = plt.subplots(figsize=(8, 4))
barres = ax.bar(cols, quadrats, color=["tab:blue", "tab:blue", "tab:orange", "tab:orange"])
ax.bar_label(barres, fmt="%.2f")
ax.set_ylabel("$(a_i - b_i)^2$")
ax.set_title(f"Suma de les barres = {quadrats.sum():.2f} = d², i d = √{quadrats.sum():.2f} = {dist_4d:.2f}")
ax.grid(alpha=0.3, axis="y")
plt.show()
"""), "ml01_barres4d"),
]))

# --- 2. Manhattan contra euclidiana
ML01_INSERCIONS.append(("manhattan = abs(x1 - x2) + abs(y1 - y2)", [
    g(md(r"""
Les dues distàncies sobre les mateixes dues flors. L'euclidiana va en línia recta (la
hipotenusa); la de Manhattan va per la quadrícula, primer en horitzontal i després en
vertical, com un taxi que no pot travessar les illes de cases.
"""), "ml01_manhattan"),
    g(code(r"""
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter([x1], [y1], color="tab:blue", s=90, zorder=3, label="flor A")
ax.scatter([x2], [y2], color="tab:orange", s=90, zorder=3, label="flor B")
ax.plot([x1, x2], [y1, y2], color="tab:red", linewidth=2,
        label=f"euclidiana = {euclidiana:.2f} cm")
ax.plot([x1, x2, x2], [y1, y1, y2], color="tab:green", linewidth=2, linestyle="--",
        label=f"Manhattan = {abs(x1 - x2):.2f} + {abs(y1 - y2):.2f} = {manhattan:.2f} cm")
ax.set_xlabel("Llargada del pètal (cm)")
ax.set_ylabel("Amplada del pètal (cm)")
ax.set_title("Dues maneres de mesurar el mateix camí")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
ax.axis("equal")
plt.show()
"""), "ml01_manhattan"),
]))

# --- 3. els k veins i el vot
ML01_INSERCIONS.append(("predit = classifica_knn(flor_prova[cols]", [
    g(md(r"""
Ho veiem en un dibuix. Per poder-ho dibuixar ens quedem només amb les dues mesures del
pètal, i posem una **flor nova inventada** (l'estrella) just a la zona on `versicolor` i
`virginica` es barregen. El cercle passa pel $k$-èsim veí: les flors de dins són les que
voten. El mateix punt, tres valors de $k$, i el vot pot canviar.
"""), "ml01_vots"),
    g(code(r"""
colors_esp = {"setosa": "tab:blue", "versicolor": "tab:orange", "virginica": "tab:green"}
P_pet = dades[["petal_llarg", "petal_ample"]].to_numpy(dtype=float)
esp = dades["especie"].to_numpy()
flor_nova = np.array([4.85, 1.70])                     # inventada, no és al dataset

d_nova = np.sqrt(np.sum((P_pet - flor_nova) ** 2, axis=1))
ordre = np.argsort(d_nova, kind="stable")

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
for ax, k_v in zip(axs, [1, 5, 15]):
    veins = ordre[:k_v]
    radi = d_nova[veins[-1]]
    for nom, color in colors_esp.items():
        m = esp == nom
        ax.scatter(P_pet[m, 0], P_pet[m, 1], color=color, s=20, alpha=0.35)
    for j in veins:
        ax.plot([flor_nova[0], P_pet[j, 0]], [flor_nova[1], P_pet[j, 1]], color="gray", linewidth=0.8)
        ax.scatter(P_pet[j, 0], P_pet[j, 1], color=colors_esp[esp[j]], s=60, edgecolor="k", zorder=3)
    ax.add_patch(plt.Circle(flor_nova, radi, fill=False, color="black", linestyle="--"))
    ax.scatter(*flor_nova, marker="*", s=350, color="tab:red", edgecolor="k", zorder=4)
    noms, vots = np.unique(esp[veins], return_counts=True)
    guanya = noms[np.argmax(vots)]
    recompte = ", ".join(f"{n} {v}" for n, v in zip(noms, vots))
    ax.set_title(f"k = {k_v}: {recompte}\n→ guanya {guanya}")
    ax.set_xlabel("Llargada del pètal (cm)")
    ax.set_xlim(3.4, 6.6)
    ax.set_ylim(0.8, 2.6)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("Amplada del pètal (cm)")
plt.tight_layout()
plt.show()
"""), "ml01_vots"),
]))

# --- 5. frontera i corba entrenament / examen
ML01_INSERCIONS.append(("Els dos extrems queden per sota dels valors del mig", [
    g(md(r"""
### Com es veu el sobreajust

Amb iris tot és massa net per veure-ho bé. Sortim-ne un moment: **dades inventades**, dues
classes barrejades en forma de mitja lluna, i les pintem amb el color que k-NN donaria a
**cada punt del pla**. Aquesta és la **frontera de decisió**.

- Amb `k=1` la frontera fa **illes**: cada punt d'entrenament s'envolta del seu color,
  encara que sigui un punt rar enmig de l'altra classe. Encerta el 100 % de l'entrenament
  perquè cada punt és el seu propi veí més proper: **memoritza**.
- Amb `k=15` la frontera és **suau**: segueix la forma general i ignora els punts solts.
- Amb `k=200` la suavitza tant que ja no segueix la forma: **infraajust**.
"""), "ml01_frontera"),
    g(code(r"""
from sklearn.datasets import make_moons

X_lluna, y_lluna = make_moons(n_samples=600, noise=0.35, random_state=4)
Xl_entrena, Xl_examen, yl_entrena, yl_examen = train_test_split(
    X_lluna, y_lluna, test_size=0.5, random_state=4, stratify=y_lluna)

gx, gy = np.meshgrid(np.linspace(-2, 3, 300), np.linspace(-1.6, 2.1, 300))
graella = np.column_stack([gx.ravel(), gy.ravel()])
from matplotlib.colors import ListedColormap
fons = ListedColormap(["#c6dbef", "#fcbba1"])          # blau i vermell suaus

fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), sharex=True, sharey=True)
for ax, k_f in zip(axs, [1, 15, 200]):
    knn_f = KNeighborsClassifier(n_neighbors=k_f).fit(Xl_entrena, yl_entrena)
    ax.contourf(gx, gy, knn_f.predict(graella).reshape(gx.shape), cmap=fons, alpha=0.9)
    ax.scatter(Xl_entrena[yl_entrena == 0, 0], Xl_entrena[yl_entrena == 0, 1],
               color="tab:blue", edgecolor="k", s=18)
    ax.scatter(Xl_entrena[yl_entrena == 1, 0], Xl_entrena[yl_entrena == 1, 1],
               color="tab:red", edgecolor="k", s=18)
    ax.set_title(f"k = {k_f}\nentrenament {knn_f.score(Xl_entrena, yl_entrena):.0%}"
                 f" · examen {knn_f.score(Xl_examen, yl_examen):.0%}")
    ax.set_xlabel("columna 1")
axs[0].set_ylabel("columna 2")
plt.tight_layout()
plt.show()
"""), "ml01_frontera"),
    g(md(r"""
Ara la mateixa pregunta del principi de l'apartat, però mesurant **dues** exactituds per a
cada $k$: la de les dades que el model ja ha vist (entrenament) i la de les que no ha vist
mai (examen).
"""), "ml01_corba"),
    g(code(r"""
valors_k_l = range(1, 271)
prec_entrena_l, prec_examen_l = [], []
for k_c in valors_k_l:
    knn_c = KNeighborsClassifier(n_neighbors=k_c).fit(Xl_entrena, yl_entrena)
    prec_entrena_l.append(knn_c.score(Xl_entrena, yl_entrena))
    prec_examen_l.append(knn_c.score(Xl_examen, yl_examen))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(list(valors_k_l), prec_entrena_l, color="tab:blue", linewidth=2, label="entrenament (ja vistes)")
ax.plot(list(valors_k_l), prec_examen_l, color="tab:orange", linewidth=2, label="examen (mai vistes)")
ax.fill_between(list(valors_k_l), prec_examen_l, prec_entrena_l, color="tab:red", alpha=0.12,
                label="distància entre les dues")
ax.axvspan(1, 6, color="tab:red", alpha=0.08)
ax.text(1.5, 0.62, "sobreajust:\nmemoritza", color="tab:red")
ax.axvspan(200, 270, color="tab:green", alpha=0.08)
ax.text(203, 0.62, "infraajust:\nho suavitza tot", color="tab:green")
ax.set_ylim(0.6, 1.01)
ax.set_xlabel("k (nombre de veïns)")
ax.set_ylabel("Exactitud")
ax.set_title("Dades inventades: exactitud a l'entrenament i a l'examen segons k")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
plt.show()
"""), "ml01_corba"),
    g(md(r"""
**Això és el sobreajust (overfitting)**: el model va molt bé amb les dades que ha vist i
pitjor amb les que no ha vist. A `k=1` la corba blava toca el 100 %, i no vol dir res: el
model ha memoritzat l'entrenament, no ha après la forma.

I per això **es parteix el conjunt** en entrenament i examen. Si només mesuréssiu la
exactitud amb les dades d'entrenament, triaríeu sempre `k=1`, que és justament el pitjor
per a dades noves. L'exactitud que val és la de l'examen, la de dades que el model no ha
vist mai, perquè és la que tindrà quan el feu servir de veritat.
"""), "ml01_sobreajust"),
]))

# --- 6. el parany de les escales
ML01_INSERCIONS.append(("Amb `StandardScaler` l'exactitud puja", [
    g(md(r"""
El parany en un dibuix. Agafem dues columnes, `petal_llarg` i `sepal_ample` ×100, i una
flor concreta (l'estrella, una `virginica`). El cercle de línia discontínua són **tots els
punts que estan a la mateixa distància que el seu veí més proper**.

- **Sense escalar** (esquerra), aquest «cercle» és una franja aplanada: l'eix vertical va
  de 200 a 450, i una diferència de 4,7 cm de pètal hi pesa com 4,7 unitats de sèpal, és a
  dir, gairebé res. El veí més proper és una `setosa`, amb un pètal quatre vegades més
  curt, només perquè té el sèpal igual.
- **Després d'estandarditzar** (dreta), les dues columnes pesen igual, el cercle torna a
  ser un cercle i el veí més proper és una altra `virginica`.
"""), "ml01_escales"),
    g(code(r"""
idx_e = 109                                             # una virginica
Q = dades[["petal_llarg", "sepal_ample"]].to_numpy(dtype=float)
Q[:, 1] *= 100
Q_esc = StandardScaler().fit_transform(Q)
colors_esp = {"setosa": "tab:blue", "versicolor": "tab:orange", "virginica": "tab:green"}
esp = dades["especie"].to_numpy()
t = np.linspace(0, 2 * np.pi, 200)

fig, axs = plt.subplots(1, 2, figsize=(14, 6))
for ax, M, titol in [(axs[0], Q, "sepal_ample ×100, sense escalar"),
                     (axs[1], Q_esc, "Després de StandardScaler")]:
    d_e = np.sqrt(np.sum((M - M[idx_e]) ** 2, axis=1))
    d_e[idx_e] = np.inf
    j = int(np.argmin(d_e))
    for nom, color in colors_esp.items():
        m = esp == nom
        ax.scatter(M[m, 0], M[m, 1], color=color, s=20, alpha=0.5, label=nom)
    ax.plot(M[idx_e, 0] + d_e[j] * np.cos(t), M[idx_e, 1] + d_e[j] * np.sin(t), "k--", linewidth=1)
    ax.plot([M[idx_e, 0], M[j, 0]], [M[idx_e, 1], M[j, 1]], color="tab:red", linewidth=2)
    ax.scatter(*M[j], color=colors_esp[esp[j]], s=110, edgecolor="k", zorder=3,
               label=f"veí més proper: {esp[j]}")
    ax.scatter(*M[idx_e], marker="*", s=350, color="tab:red", edgecolor="k", zorder=4,
               label="la flor (virginica)")
    ax.set_title(titol)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=9)
axs[0].set_xlabel("petal_llarg (cm)")
axs[0].set_ylabel("sepal_ample × 100")
axs[1].set_xlabel("petal_llarg estandarditzat")
axs[1].set_ylabel("sepal_ample estandarditzat")
axs[1].set_aspect("equal", adjustable="datalim")
plt.tight_layout()
plt.show()
"""), "ml01_escales"),
]))

# --- 7. il.lustratius abans de cada exercici (s'insereixen DAVANT la cel.la de codi)
ML01_EXERCICIS = []

ML01_EXERCICIS.append(("# Exercici 1\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: seixanta punts inventats al voltant d'un centre.
Pintem de fosc els que són a distància menor que 1. Amb l'euclidiana, «a distància 1» és un
**cercle**; amb Manhattan, és un **rombe**. Per això dues distàncies poden triar veïns
diferents.
"""), "ml01_il1"),
    g(code(r"""
rng = np.random.default_rng(1)
punts_il = rng.uniform(-1.4, 1.4, size=(60, 2))          # punts inventats
eucl_il = np.sqrt(np.sum(punts_il ** 2, axis=1))
manh_il = np.sum(np.abs(punts_il), axis=1)
t_il = np.linspace(0, 2 * np.pi, 200)

fig, axs = plt.subplots(1, 2, figsize=(11, 5))
for ax, dist_il, nom, vora in [(axs[0], eucl_il, "euclidiana", (np.cos(t_il), np.sin(t_il))),
                               (axs[1], manh_il, "Manhattan", ([1, 0, -1, 0, 1], [0, 1, 0, -1, 0]))]:
    dins = dist_il < 1
    ax.scatter(punts_il[~dins, 0], punts_il[~dins, 1], color="lightgray", edgecolor="gray", s=40)
    ax.scatter(punts_il[dins, 0], punts_il[dins, 1], color="tab:blue", edgecolor="k", s=40)
    ax.plot(*vora, color="tab:red", linewidth=2)
    ax.scatter([0], [0], marker="*", s=300, color="tab:red", edgecolor="k", zorder=3)
    ax.set_title(f"Dades inventades: distància {nom} < 1 ({dins.sum()} punts)")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""), "ml01_il1"),
]))

ML01_EXERCICIS.append(("# Exercici 2\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: exactituds inventades per a 30 valors de `k` i
com les ha de llegir el vostre bucle. Compte amb el parany: `np.argmax` torna la
**posició** a la llista, que comença a 0, mentre que `k` comença a 1.
"""), "ml01_il2"),
    g(code(r"""
rng = np.random.default_rng(4)
ks_il = np.arange(1, 31)
prec_il = 0.80 + 0.08 * np.exp(-((ks_il - 18) / 9) ** 2) + rng.normal(0, 0.01, 30)  # inventades

pos_il = int(np.argmax(prec_il))
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(ks_il, prec_il, marker="o", color="tab:blue")
ax.scatter([ks_il[pos_il]], [prec_il[pos_il]], s=200, facecolor="none", edgecolor="tab:red", linewidth=2)
ax.annotate(f"argmax = posició {pos_il}\n→ k = {ks_il[pos_il]}", (ks_il[pos_il], prec_il[pos_il]),
            xytext=(ks_il[pos_il] - 12, prec_il[pos_il] - 0.03),
            arrowprops=dict(arrowstyle="->", color="tab:red"), color="tab:red")
ax.set_xlabel("k")
ax.set_ylabel("exactitud (inventada)")
ax.set_title("Dades inventades: el bucle es queda amb el màxim")
ax.grid(alpha=0.3)
plt.show()
"""), "ml01_il2"),
]))

ML01_EXERCICIS.append(("# Exercici 3\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: el paràmetre `metric` canvia **qui** són els
veïns, no com voten. El mateix punt nou (l'estrella) entre punts inventats, i els seus 5
veïns segons cada distància. Els encerclats en vermell només són veïns amb una de les dues.
"""), "ml01_il4"),
    g(code(r"""
rng = np.random.default_rng(11)
pts_il = rng.uniform(0, 4, size=(40, 2))                 # punts inventats
nou_il = np.array([2.0, 2.0])
v_eu = set(np.argsort(np.sqrt(np.sum((pts_il - nou_il) ** 2, axis=1)))[:5])
v_ma = set(np.argsort(np.sum(np.abs(pts_il - nou_il), axis=1))[:5])

fig, axs = plt.subplots(1, 2, figsize=(11, 5))
for ax, veins_il, nom in [(axs[0], v_eu, 'metric="euclidean"'), (axs[1], v_ma, 'metric="manhattan"')]:
    ax.scatter(pts_il[:, 0], pts_il[:, 1], color="lightgray", edgecolor="gray", s=40)
    for j in veins_il:
        ax.plot([nou_il[0], pts_il[j, 0]], [nou_il[1], pts_il[j, 1]], color="tab:blue", linewidth=1)
        ax.scatter(*pts_il[j], color="tab:blue", edgecolor="k", s=60, zorder=3)
        if j not in (v_eu & v_ma):
            ax.scatter(*pts_il[j], s=250, facecolor="none", edgecolor="tab:red", linewidth=2, zorder=4)
    ax.scatter(*nou_il, marker="*", s=300, color="tab:red", edgecolor="k", zorder=5)
    ax.set_title(f"Dades inventades: 5 veïns amb {nom}")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""), "ml01_il4"),
]))


# =====================================================================  EX_01
EX01_EXERCICIS = []

EX01_EXERCICIS.append(("# Exercici 1\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: tres columnes inventades, cadascuna amb el seu
interval del mínim al màxim, totes sobre el **mateix** eix. Quan una columna va per
centenars, les que van per unitats es veuen com un punt. Això és el que heu de buscar al
`describe()`: no el valor de cada columna, sinó **com de diferents són els rangs**.
"""), "ex01_il1"),
    g(code(r"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
cols_il = {"col_centenars": rng.normal(500, 150, 100),   # dades inventades
           "col_desenes": rng.normal(40, 8, 100),
           "col_unitats": rng.normal(1.5, 0.4, 100)}

fig, ax = plt.subplots(figsize=(9, 3.5))
for fila, (nom, v) in enumerate(cols_il.items()):
    ax.plot([v.min(), v.max()], [fila, fila], color="tab:blue", linewidth=6, solid_capstyle="butt")
    ax.text(v.max() + 10, fila, f"de {v.min():.1f} a {v.max():.1f}", va="center")
ax.set_yticks(range(3), list(cols_il))
ax.set_xlim(-20, 1100)
ax.set_xlabel("valor (mateix eix per a totes)")
ax.set_title("Dades inventades: el min i el max del describe(), dibuixats")
ax.grid(alpha=0.3, axis="x")
plt.show()
"""), "ex01_il1"),
]))

EX01_EXERCICIS.append(("# Exercici 2\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: què fa `stratify`. Cent etiquetes inventades de
tres classes, partides 70/30 dues vegades. Sense `stratify` l'examen pot quedar amb una
proporció de classes diferent de la del conjunt sencer; amb `stratify` les tres barres
queden iguals. És la comprovació que us demanem amb `value_counts(normalize=True)`.
"""), "ex01_il2"),
    g(code(r"""
from sklearn.model_selection import train_test_split

y_il = np.array(["A"] * 50 + ["B"] * 35 + ["C"] * 15)   # etiquetes inventades
X_il = np.arange(100).reshape(-1, 1)
_, _, _, ye_sense = train_test_split(X_il, y_il, test_size=0.3, random_state=3)
_, _, _, ye_amb = train_test_split(X_il, y_il, test_size=0.3, random_state=3, stratify=y_il)

def proporcions_il(v):
    return [np.mean(v == c) for c in ["A", "B", "C"]]

fig, ax = plt.subplots(figsize=(9, 4))
amplada = 0.27
for i, (nom, v, color) in enumerate([("conjunt sencer", y_il, "tab:blue"),
                                     ("examen sense stratify", ye_sense, "tab:red"),
                                     ("examen amb stratify", ye_amb, "tab:green")]):
    ax.bar(np.arange(3) + (i - 1) * amplada, proporcions_il(v), amplada, color=color, label=nom)
ax.set_xticks(range(3), ["classe A", "classe B", "classe C"])
ax.set_ylabel("proporció")
ax.set_title("Dades inventades: proporcions de classe a l'examen")
ax.legend()
ax.grid(alpha=0.3, axis="y")
plt.show()
"""), "ex01_il2"),
]))

EX01_EXERCICIS.append(("# Exercici 3\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: com es comprova que l'escalat s'ha fet bé. Tres
columnes inventades, escalades amb un `StandardScaler` ajustat només amb l'entrenament. A
l'entrenament les mitjanes surten 0 i les desviacions 1 exactes; a l'examen, a prop però
no exactes. Si a l'entrenament no us surt així, no compareu cap exactitud.
"""), "ex01_il3"),
    g(code(r"""
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(2)
M_il = np.column_stack([rng.normal(500, 150, 120), rng.normal(40, 8, 120), rng.normal(1.5, 0.4, 120)])
Me_il, Mx_il = M_il[:84], M_il[84:]                      # 70/30, dades inventades
esc_il = StandardScaler().fit(Me_il)
Me_esc_il, Mx_esc_il = esc_il.transform(Me_il), esc_il.transform(Mx_il)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
pos_il = np.arange(3)
for ax, funcio, nom, objectiu in [(axs[0], np.mean, "mitjana", 0), (axs[1], np.std, "desviació", 1)]:
    ax.bar(pos_il - 0.2, funcio(Me_esc_il, axis=0), 0.4, color="tab:blue", label="entrenament escalat")
    ax.bar(pos_il + 0.2, funcio(Mx_esc_il, axis=0), 0.4, color="tab:orange", label="examen escalat")
    ax.axhline(objectiu, color="black", linestyle="--", linewidth=1)
    ax.set_xticks(pos_il, ["col 1", "col 2", "col 3"])
    ax.set_title(f"Dades inventades: {nom} per columna\n(a l'entrenament, exactament {objectiu})")
    ax.grid(alpha=0.3, axis="y")
axs[0].legend(loc="upper left")
plt.tight_layout()
plt.show()
"""), "ex01_il3"),
]))

EX01_EXERCICIS.append(("# Exercici 4\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: per què la desviació estàndard d'una columna diu
quant pesarà a la distància. Dues columnes inventades: per a moltes parelles de files, la
diferència $|a_i - b_i|$ en cadascuna. La columna amb més desviació dona diferències més
grans, i a la distància aquestes diferències s'eleven al quadrat.
"""), "ex01_il4"),
    g(code(r"""
rng = np.random.default_rng(6)
gran_il = rng.normal(500, 150, 300)                      # desviació ~150
petita_il = rng.normal(1.5, 0.4, 300)                    # desviació ~0.4
i_il, j_il = rng.integers(0, 300, 1000), rng.integers(0, 300, 1000)

dif_gran_il = np.abs(gran_il[i_il] - gran_il[j_il])
dif_petita_il = np.abs(petita_il[i_il] - petita_il[j_il])
calaixos_il = np.linspace(0, 700, 71)                  # els mateixos calaixos per a totes dues

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(dif_gran_il, bins=calaixos_il, color="tab:orange", alpha=0.7,
        label=f"columna amb desviació {gran_il.std():.0f}")
ax.hist(dif_petita_il, bins=calaixos_il, color="tab:blue", alpha=0.9,
        label=f"columna amb desviació {petita_il.std():.1f}")
ax.set_ylim(0, 140)
ax.annotate(f"les {len(dif_petita_il)} diferències de la columna petita\ncauen totes aquí (cap passa de {dif_petita_il.max():.1f})",
            (5, 135), xytext=(150, 110), arrowprops=dict(arrowstyle="->", color="tab:blue"), color="tab:blue")
ax.set_xlabel("diferència entre dues files, |a - b|")
ax.set_ylabel("parelles")
ax.set_title("Dades inventades: la desviació mana la mida de les diferències")
ax.legend()
ax.grid(alpha=0.3)
plt.show()
"""), "ex01_il4"),
]))

EX01_EXERCICIS.append(("# Exercici 5\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: com es llegeix la taula contra el model tonto.
Cinc models inventats (no són els vostres) i la línia del `DummyClassifier`, que sempre
diu la classe més nombrosa. Un model que queda per sota de la línia no ha après res: està
mal entrenat o li heu passat dades equivocades.
"""), "ex01_il5"),
    g(code(r"""
prec_models_il = {"model A": 0.91, "model B": 0.84, "model C": 0.33, "model D": 0.77, "model E": 0.88}
dummy_il = 0.45                                          # tot inventat

noms_il = list(prec_models_il)
valors_il = np.array(list(prec_models_il.values()))
fig, ax = plt.subplots(figsize=(9, 4))
ax.barh(noms_il, valors_il, color=np.where(valors_il < dummy_il, "tab:red", "tab:blue"))
ax.axvline(dummy_il, color="black", linestyle="--", label="DummyClassifier (classe més nombrosa)")
ax.set_xlim(0, 1)
ax.set_xlabel("exactitud a l'examen (inventada)")
ax.set_title("Dades inventades: en vermell, el que no guanya el model tonto")
ax.legend(loc="lower right")
ax.grid(alpha=0.3, axis="x")
plt.show()
"""), "ex01_il5"),
]))

EX01_EXERCICIS.append(("# Exercici 6\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: què vol dir `max_depth`. Punts inventats de tres
classes i el color que posa l'arbre a cada zona del pla, amb profunditat 1, 3 i sense
límit. Amb `max_depth=1` només hi ha un tall, dues fulles i, per tant, una classe que no
surt mai. Sense límit, l'arbre talla fins a encerclar cada punt solt. La corba que
dibuixareu mesura on passa de l'un a l'altre amb Wine.
"""), "ex01_il6"),
    g(code(r"""
from sklearn.datasets import make_blobs
from sklearn.tree import DecisionTreeClassifier
from matplotlib.colors import ListedColormap

Xb_il, yb_il = make_blobs(n_samples=150, centers=[[0, 0], [4, 0], [2, 3.5]],
                          cluster_std=1.5, random_state=0)  # inventades
gx_il, gy_il = np.meshgrid(np.linspace(Xb_il[:, 0].min() - 1, Xb_il[:, 0].max() + 1, 300),
                           np.linspace(Xb_il[:, 1].min() - 1, Xb_il[:, 1].max() + 1, 300))
graella_il = np.column_stack([gx_il.ravel(), gy_il.ravel()])
fons_il = ListedColormap(["#c6dbef", "#fdd0a2", "#c7e9c0"])
punts_col = ["tab:blue", "tab:orange", "tab:green"]

fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), sharex=True, sharey=True)
for ax, prof in zip(axs, [1, 3, None]):
    arbre_il = DecisionTreeClassifier(max_depth=prof, random_state=0).fit(Xb_il, yb_il)
    ax.contourf(gx_il, gy_il, arbre_il.predict(graella_il).reshape(gx_il.shape),
                levels=[-0.5, 0.5, 1.5, 2.5], cmap=fons_il)
    for c in range(3):
        ax.scatter(Xb_il[yb_il == c, 0], Xb_il[yb_il == c, 1], color=punts_col[c], edgecolor="k", s=18)
    ax.set_title(f"max_depth={prof}\n{arbre_il.get_n_leaves()} fulles · "
                 f"{len(np.unique(arbre_il.predict(Xb_il)))} classes predites")
plt.tight_layout()
plt.show()
"""), "ex01_il6"),
]))

EX01_EXERCICIS.append(("# Exercici 7\n", [
    g(md(r"""
Abans de començar, la idea en un dibuix: com es llegeix `feature_importances_`. Cinc
importàncies inventades: sumen 1, i en un `barh` la primera fila de la `Series` queda
**a baix**. Per això, si ordeneu de petita a gran amb `.sort_values()`, la més important
surt a dalt de tot.
"""), "ex01_il7"),
    g(code(r"""
import pandas as pd

imp_il = pd.Series([0.05, 0.40, 0.10, 0.30, 0.15],
                   index=["col_a", "col_b", "col_c", "col_d", "col_e"])   # inventades

fig, axs = plt.subplots(1, 2, figsize=(12, 3.8))
imp_il.plot(kind="barh", ax=axs[0], color="lightgray", edgecolor="gray")
axs[0].set_title("Sense ordenar")
imp_il.sort_values().plot(kind="barh", ax=axs[1], color="tab:blue")
axs[1].set_title(f"Amb .sort_values() (suma = {imp_il.sum():.2f})")
for ax in axs:
    ax.set_xlabel("importància (inventada)")
    ax.grid(alpha=0.3, axis="x")
plt.tight_layout()
plt.show()
"""), "ex01_il7"),
]))


# =====================================================================  motor
def llegeix(ruta):
    return json.load(io.open(ruta, encoding="utf-8"))


def desa(nb, ruta):
    io.open(ruta, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


def troba(cells, text):
    trobades = [i for i, c in enumerate(cells) if text in "".join(c["source"])]
    if len(trobades) != 1:
        raise SystemExit(f"ancora ambigua o absent ({len(trobades)}): {text!r}")
    return trobades[0]


def aplica(ruta, despres=(), davant=(), marca_ex=False):
    nb = llegeix(ruta)
    cells = [c for c in nb["cells"] if "grafic" not in c.get("metadata", {})]
    for ancora, noves in despres:
        i = troba(cells, ancora)
        cells[i + 1:i + 1] = noves
    for ancora, noves in davant:
        i = troba(cells, ancora)
        if marca_ex:
            tags = cells[i]["metadata"].setdefault("tags", [])
            if "exercici" not in tags:
                tags.append("exercici")
        cells[i:i] = noves
    nb["cells"] = cells
    desa(nb, ruta)
    n = sum(1 for c in cells if "grafic" in c["metadata"] and c["cell_type"] == "code")
    print(f"{ruta}: {len(cells)} cel.les, {n} grafics nous")


def neteja(ruta):
    """Treu sortides i comptador de les cel.les d'exercici (han de quedar buides)."""
    nb = llegeix(ruta)
    for c in nb["cells"]:
        if c["cell_type"] == "code" and "exercici" in c["metadata"].get("tags", []):
            c["outputs"], c["execution_count"] = [], None
    desa(nb, ruta)


if __name__ == "__main__":
    if "--neteja" in sys.argv:
        neteja(ML01)
        neteja(EX01)
    else:
        aplica(ML01, despres=ML01_INSERCIONS, davant=ML01_EXERCICIS, marca_ex=True)
        aplica(EX01, davant=EX01_EXERCICIS)
