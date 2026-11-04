# -*- coding: utf-8 -*-
"""Afegeix els grafics a ML_04_regressio_logistica.ipynb (quadern sense generador).

Llegeix el quadern, treu les cel.les que hi havia posat aquest mateix script
(porten `metadata.afegit = "grafics_ML_04"`, aixi es pot tornar a executar sense
duplicar res) i insereix les noves just despres de les cel.les ancora, que es
troben pel text i no per la posicio.

Teoria: com mouen w i b la sigmoide; les tres flors sobre la sigmoide; el pla z i
la seva sigmoide en 3D; la perdua segons la probabilitat de la classe correcta
(log-loss contra error quadratic); el paisatge en 3D; el mapa de probabilitat de
la frontera; les tres probabilitats amb tres especies.
Exercicis: un grafic il.lustratiu amb dades inventades abans de cadascun.

    python _eines/grafics_ML_04.py
"""
import io
import json
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code

QUADERN = "Machine Learning/01_teoria/ML_04_regressio_logistica.ipynb"
MARCA = "grafics_ML_04"


def marcades(*cels):
    for c in cels:
        c["metadata"]["afegit"] = MARCA
    return list(cels)


INSERCIONS = []   # (text que identifica l'ancora, cel.les a posar despres)


# ------------------------------------------------- 2.2 com mouen w i b la sigmoide
INSERCIONS.append(('plt.title("La funció sigmoide")', marcades(md(r"""
#### Com la mouen $w$ i $b$

Mirem-ho primer amb una sola columna. $z = w\,x + b$ és **la recta de `MA_01b`**, i la
sigmoide s'hi posa a sobre: $p = \sigma(w\,x + b)$. Tres petits múltiples:

- **$w$ estira**: com més gran, més dreta és la S i més de pressa passa de 0 a 1.
- **$b$ desplaça**: el punt on val 0,5 és on $z = 0$, és a dir, a $x = -b/w$.
- **$w$ negatiu la gira**: ara les $x$ grans donen probabilitats petites.
"""), code(r"""
x_il = np.linspace(2, 8, 300)       # una sola columna inventada, en cm

fig, eixos = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
for w, color in [(0.5, "tab:blue"), (1, "tab:orange"), (3, "tab:red")]:
    eixos[0].plot(x_il, sigmoide(w * x_il - 5 * w), color=color, linewidth=2,
                  label=f"w = {w}, b = {-5 * w:g}")
eixos[0].set_title("$w$ estira (el centre, quiet a 5 cm)")

for b, color in [(-8, "tab:blue"), (-10, "tab:orange"), (-12, "tab:red")]:
    eixos[1].plot(x_il, sigmoide(2 * x_il + b), color=color, linewidth=2,
                  label=f"w = 2, b = {b}: centre a {-b / 2:g} cm")
eixos[1].set_title("$b$ desplaça: el centre és a $x = -b/w$")

for w, b, color in [(2, -10, "tab:orange"), (-2, 10, "tab:green")]:
    eixos[2].plot(x_il, sigmoide(w * x_il + b), color=color, linewidth=2,
                  label=f"w = {w}, b = {b}")
eixos[2].set_title("$w$ negatiu la gira")

for ax in eixos:
    ax.axhline(0.5, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("$x$ (una columna)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
eixos[0].set_ylabel(r"$p = \sigma(w\,x + b)$")
plt.tight_layout()
plt.show()
"""))))

# ------------------------------------------------- 2.3 les tres flors sobre la sigmoide
INSERCIONS.append(('flors = pd.DataFrame(', marcades(md(r"""
#### De la recta a la probabilitat

Les tres flors sobre la sigmoide. Cada una cau a la seva $z$ (eix horitzontal: de quin
costat de la recta és i com d'endins) i la corba la converteix en probabilitat de
virginica (eix vertical).
"""), code(r"""
colors_flors = ["tab:orange", "gray", "tab:green"]
z_vals = np.linspace(-6, 6, 300)

plt.figure(figsize=(8, 4.8))
plt.plot(z_vals, sigmoide(z_vals), color="tab:red", linewidth=2)
for (_, fila), color in zip(flors.iterrows(), colors_flors):
    zf, pf = fila["z"], fila["sigma(z)"]
    plt.plot([zf, zf], [0, pf], color=color, linestyle="--", linewidth=1)
    plt.plot([-6, zf], [pf, pf], color=color, linestyle="--", linewidth=1)
    plt.scatter([zf], [pf], color=color, s=80, edgecolor="k", zorder=5,
                label=f"{fila['flor']}: z = {zf:.1f}  →  p = {pf:.3f}")
plt.axvline(0, color="gray", linestyle=":", linewidth=1)
plt.xlabel("$z = w_1 x_1 + w_2 x_2 + b$  (de quin costat de la recta, i com d'endins)")
plt.ylabel(r"$p = \sigma(z)$, probabilitat de virginica")
plt.title("Tres flors: de la recta a la probabilitat")
plt.legend(loc="upper left", fontsize=9)
plt.grid(alpha=0.3)
plt.show()
"""), md(r"""
I amb les dues columnes alhora, en 3D. A l'esquerra, $z = x_1 + x_2 - 6{,}5$ és **un pla**,
com el de l'exercici 3 de `MA_01b`, i cada flor hi és a la seva $z$. A la dreta, el mateix
pla passat per la sigmoide: es doblega en un esglaó suau entre 0 i 1, i cada flor hi és a
la seva alçada real, 0 (versicolor) o 1 (virginica). La línia negra és la recta del
gràfic de la secció 2.1, on $z = 0$ i $p = 0{,}5$.
"""), code(r"""
g1, g2 = np.meshgrid(np.linspace(2.8, 7.2, 40), np.linspace(0.9, 2.6, 40))
pla_z = w1_ma * g1 + w2_ma * g2 + b_ma
z_flors = w1_ma * bi["petal_llarg"] + w2_ma * bi["petal_ample"] + b_ma
col_flors = bi["especie"].map(colors_bi)
x1_recta = np.linspace(4.0, 5.6, 2)               # tros de la recta x1 + x2 = 6,5 dins la graella

fig = plt.figure(figsize=(13, 5.5))
for k, (sup, alcada, recta_h, nom_z, titol) in enumerate([
        (pla_z, z_flors, 0.0, "$z$", "La recta de MA_01b, ara un pla: $z$"),
        (sigmoide(pla_z), bi["y"], 0.5, "$p$", r"El pla passat per la sigmoide: $p = \sigma(z)$")]):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d")
    ax.plot_surface(g1, g2, sup, color="tab:blue", alpha=0.18, linewidth=0)
    ax.scatter(bi["petal_llarg"], bi["petal_ample"], alcada, c=col_flors, edgecolor="k",
               s=22, depthshade=False)
    ax.plot(x1_recta, 6.5 - x1_recta, [recta_h, recta_h], color="black", linewidth=3)
    ax.set_xlabel("llargada (cm)")
    ax.set_ylabel("amplada (cm)")
    ax.set_zlabel(nom_z)
    ax.view_init(elev=22, azim=-125)
    ax.set_box_aspect(None, zoom=0.85)
    ax.set_title(titol)
plt.tight_layout()
plt.show()
"""))))

# ------------------------------------------------- 3 log-loss contra error quadratic
INSERCIONS.append(("## 3. Com s'aprenen els pesos", marcades(code(r"""
p_correcta = np.linspace(0.001, 1, 400)      # probabilitat que el model dona a la classe real

plt.figure(figsize=(8, 4.8))
plt.plot(p_correcta, -np.log(p_correcta), color="tab:blue", linewidth=2,
         label=r"log-loss: $-\log p$")
plt.plot(p_correcta, (1 - p_correcta) ** 2, color="tab:orange", linewidth=2,
         label="error quadràtic (el MSE de MA_01b): $(1 - p)^2$")
for p_punt, text, lloc in [(0.49, "0,51 a la classe equivocada", (0.45, 1.6)),
                          (0.01, "0,99 a la classe equivocada", (0.1, 4.2))]:
    plt.scatter([p_punt], [-np.log(p_punt)], color="tab:blue", edgecolor="k", zorder=5)
    plt.annotate(f"{text}: costa {-np.log(p_punt):.2f}".replace(".", ","),
                 (p_punt, -np.log(p_punt)), xytext=lloc,
                 arrowprops=dict(arrowstyle="->", color="gray"))
plt.ylim(0, 5)
plt.xlabel("$p$, probabilitat que el model dona a la classe correcta")
plt.ylabel("pèrdua d'aquesta flor")
plt.title("Quant costa una flor, segons la probabilitat que li dona el model")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""), md(r"""
Les dues pèrdues valen 0 quan el model encerta amb tota seguretat ($p = 1$). La diferència
és a l'esquerra. Amb l'error quadràtic de `MA_01b`, equivocar-se del tot costa com a molt
1. Amb la log-loss el cost no té sostre: la flor a la qual el model dona un 0,99 a la
classe equivocada costa 4,61, més de sis vegades el que costa la dubtosa (0,71). Per això
per classificar es fa servir la log-loss i no el MSE. (Hi ha una segona raó, la del
gradient, i la veureu a `MA_02`.)
"""))))

# ------------------------------------------------- 3 paisatge en 3D
INSERCIONS.append(('plt.title("El paisatge de la pèrdua")', marcades(md(r"""
El mateix paisatge en 3D, com el del MSE a `MA_01b`: a terra els dos pesos, en alçada la
pèrdua. L'estrella vermella és el punt de scikit-learn.
"""), code(r"""
fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(projection="3d")
ax.plot_surface(W1, W2, L, cmap="viridis", rstride=2, cstride=2, linewidth=0, alpha=0.75)
ax.scatter([w1_sk], [w2_sk], [perdua_sk], color="red", marker="*", s=250, edgecolor="k",
           depthshade=False, label="Pesos trobats per scikit-learn")
ax.set_xlabel("$w_1$ (llargada)")
ax.set_ylabel("$w_2$ (amplada)")
ax.set_zlabel("pèrdua (log-loss)")
ax.view_init(elev=35, azim=-60)
ax.set_box_aspect(None, zoom=0.85)
ax.set_title("El paisatge de la pèrdua, en 3D")
ax.legend(loc="upper left")
plt.show()
"""))))

# ------------------------------------------------- 4 mapa de probabilitat
INSERCIONS.append(("La recta que dibuixa `LogisticRegression`", marcades(md(r"""
La recta no ho diu tot. El model dona una **probabilitat** a cada punt del pla, i la podem
pintar: taronja, segur que és versicolor; verd, segur que és virginica; blanc, dubte. La
línia gruixuda és la frontera, on la probabilitat val 0,5; les fines són on val 0,1 i 0,9.
"""), code(r"""
from matplotlib.colors import LinearSegmentedColormap

cmap_bi = LinearSegmentedColormap.from_list("bi", ["tab:orange", "white", "tab:green"])
G1, G2 = np.meshgrid(np.linspace(2.8, 7.2, 300), np.linspace(0.9, 2.7, 300))
P_pla = model.predict_proba(np.column_stack([G1.ravel(), G2.ravel()]))[:, 1].reshape(G1.shape)

plt.figure(figsize=(8.5, 5.5))
cf = plt.contourf(G1, G2, P_pla, levels=np.linspace(0, 1, 11), cmap=cmap_bi)
plt.colorbar(cf, label="probabilitat de virginica")
linies = plt.contour(G1, G2, P_pla, levels=[0.1, 0.5, 0.9], colors="black",
                     linewidths=[0.8, 2.2, 0.8])
plt.clabel(linies, fmt="%.1f")
for especie, grup in bi.groupby("especie"):
    plt.scatter(grup["petal_llarg"], grup["petal_ample"], label=especie,
                color=colors_bi[especie], s=40, edgecolor="k", linewidth=0.5)
plt.xlabel("Llargada del pètal (cm)")
plt.ylabel("Amplada del pètal (cm)")
plt.title("El que dona el model: una probabilitat a cada punt")
plt.legend(loc="upper left")
plt.show()
"""), md(r"""
La franja clara del mig és on el model dubta, i és justament on les dues espècies es
barregen. Lluny de la recta el color se satura: és la sigmoide aplanant-se a 0 o a 1. Les
línies de 0,1 i 0,9 són paral·leles a la frontera, perquè la probabilitat només depèn de
$z$, i $z$ és constant al llarg de cada recta paral·lela.
"""))))

# ------------------------------------------------- 5 tres especies
INSERCIONS.append(("Mireu la columna `suma`", marcades(md(r"""
Les tres probabilitats, en un dibuix. Cada panell pinta la probabilitat d'una espècie a
cada punt del pla; l'últim, l'espècie que guanya (la de probabilitat més alta), que és la
que respon `predict`. Com més fosc, més probable.
"""), code(r"""
H1, H2 = np.meshgrid(np.linspace(0.8, 7.2, 250), np.linspace(0, 2.7, 250))
probs_pla = model3.predict_proba(np.column_stack([H1.ravel(), H2.ravel()]))

fig, eixos = plt.subplots(1, 4, figsize=(17, 4), sharey=True)
mapes = {"setosa": "Blues", "versicolor": "Oranges", "virginica": "Greens"}
for k, especie in enumerate(model3.classes_):
    ax = eixos[k]
    cf = ax.contourf(H1, H2, probs_pla[:, k].reshape(H1.shape), levels=np.linspace(0, 1, 11),
                     cmap=mapes[especie])
    ax.set_title(f"P({especie})")
guanya = probs_pla.argmax(axis=1).reshape(H1.shape)
eixos[3].contourf(H1, H2, guanya, levels=[-0.5, 0.5, 1.5, 2.5],
                  colors=[colors3[e] for e in model3.classes_], alpha=0.35)
eixos[3].set_title("L'espècie que guanya")
for ax in eixos:
    for especie, grup in dades.groupby("especie"):
        ax.scatter(grup["petal_llarg"], grup["petal_ample"], color=colors3[especie],
                   s=12, edgecolor="k", linewidth=0.3)
    ax.set_xlabel("Llargada del pètal (cm)")
eixos[0].set_ylabel("Amplada del pètal (cm)")
plt.show()
"""))))

# ------------------------------------------------- exercicis: il.lustratius
INSERCIONS.append(("### Exercici 1 — La sigmoide, tu sol", marcades(md(r"""
Abans de començar, la idea en un dibuix: com dibuixa `plt.plot` una corba. No dibuixa la
funció: **uneix amb segments els punts que li doneu**. Amb pocs punts de `np.linspace`
surt a trossos; amb molts, sembla llisa. I `plt.scatter` posa un punt on li digueu. La
funció és una altra, inventada.
"""), code(r"""
f_il = lambda t: np.sin(t) + 0.3 * t           # una funcio inventada, no la sigmoide

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
for ax, n in [(ax1, 7), (ax2, 200)]:
    t_il = np.linspace(-6, 6, n)
    ax.plot(t_il, f_il(t_il), "o-" if n < 20 else "-", color="tab:blue", markersize=5)
    ax.scatter([0], [f_il(0)], color="tab:red", s=80, zorder=5, label="un punt marcat a (0, f(0))")
    ax.set_title(f"np.linspace(-6, 6, {n})")
    ax.set_xlabel("$t$")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))))

INSERCIONS.append(("### Exercici 2 — Calcula la probabilitat a mà", marcades(md(r"""
Abans de començar, la idea en un dibuix: el camí d'una flor fins a la probabilitat, amb
pesos i una flor **inventats** ($w_1 = 0{,}8$, $w_2 = 1{,}5$, $b = -6$, pètal de 4,0 × 1,2
cm). Primer la recta dona $z$; després la sigmoide converteix $z$ en $p$. Vosaltres feu el
mateix amb els pesos de `model` i la flor de l'enunciat.
"""), code(r"""
w1_il, w2_il, b_il = 0.8, 1.5, -6.0            # pesos inventats, no els de model
flor_il = (4.0, 1.2)                           # flor inventada
z_il = w1_il * flor_il[0] + w2_il * flor_il[1] + b_il
p_il = sigmoide(z_il)

zs_il = np.linspace(-6, 6, 300)
plt.figure(figsize=(8, 4.5))
plt.plot(zs_il, sigmoide(zs_il), color="tab:red", linewidth=2)
plt.annotate("", xy=(z_il, p_il), xytext=(z_il, 0),
             arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=2))
plt.annotate("", xy=(-6, p_il), xytext=(z_il, p_il),
             arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=2))
plt.scatter([z_il], [p_il], color="black", zorder=5)
plt.text(0.5, 0.15, f"1) z = {w1_il}·{flor_il[0]} + {w2_il}·{flor_il[1]} + ({b_il}) = {z_il:.2f}\n"
         f"2) p = σ({z_il:.2f}) = {p_il:.3f}", fontsize=10,
         bbox=dict(facecolor="white", edgecolor="gray"))
plt.xlabel("$z$")
plt.ylabel(r"$\sigma(z)$")
plt.title("Pesos i flor inventats: primer $z$, després $\\sigma(z)$")
plt.grid(alpha=0.3)
plt.show()
"""))))

INSERCIONS.append(("### Exercici 3 — El paràmetre `C`", marcades(md(r"""
Abans de començar, la idea en un dibuix: com es dibuixen diverses fronteres al mateix
gràfic. Cada model té el seu $w_1$, $w_2$ i $b$, i la seva recta és
$x_2 = -(w_1 x_1 + b)/w_2$, la fórmula de la secció 4. Aquí el núvol i els pesos són
inventats: tres models «A», «B» i «C» que no surten de cap entrenament. Un color i una
etiqueta per a cada un, i la llegenda fa la resta.
"""), code(r"""
rng = np.random.default_rng(4)
nuvol_0 = rng.normal([2, 2], 0.6, size=(30, 2))          # dues classes inventades
nuvol_1 = rng.normal([4, 3.5], 0.6, size=(30, 2))
models_il = {"A": (1.0, 1.0, -5.8), "B": (1.5, 0.5, -6.2), "C": (0.4, 1.2, -4.6)}

plt.figure(figsize=(7.5, 5))
plt.scatter(nuvol_0[:, 0], nuvol_0[:, 1], color="tab:orange", edgecolor="k", s=30, label="classe 0")
plt.scatter(nuvol_1[:, 0], nuvol_1[:, 1], color="tab:green", edgecolor="k", s=30, label="classe 1")
x1_il = np.linspace(0, 6, 50)
for (nom, (a1, a2, bb)), color in zip(models_il.items(), ["tab:blue", "tab:red", "tab:purple"]):
    plt.plot(x1_il, -(a1 * x1_il + bb) / a2, color=color, linewidth=2,
             label=f"model {nom}: w = ({a1}, {a2}), b = {bb}")
plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel("$x_1$ (inventada)")
plt.ylabel("$x_2$ (inventada)")
plt.title("Dades inventades: tres fronteres en un sol gràfic")
plt.legend(fontsize=8, loc="upper left")
plt.grid(alpha=0.3)
plt.show()
"""))))

INSERCIONS.append(("### Exercici 4 — Altres columnes", marcades(md(r"""
Abans de començar, la idea en un dibuix: dos gràfics costat a costat amb
`plt.subplots(1, 2)`. A l'esquerra, el núvol de punts pintat per classe; a la dreta, el
mateix núvol amb la frontera d'un `LogisticRegression` i la seva precisió al títol. Les
dades són inventades; vosaltres ho feu amb les columnes del sèpal i ho poseu al costat del
que ja teniu del pètal.
"""), code(r"""
rng = np.random.default_rng(8)
X_il = np.vstack([rng.normal([3, 3], 0.8, size=(40, 2)), rng.normal([4.5, 4], 0.8, size=(40, 2))])
y_il = np.repeat([0, 1], 40)
model_il = LogisticRegression().fit(X_il, y_il)
a1, a2 = model_il.coef_[0]
bb = model_il.intercept_[0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), sharex=True, sharey=True)
for ax in (ax1, ax2):
    for classe, color in [(0, "tab:orange"), (1, "tab:green")]:
        ax.scatter(X_il[y_il == classe, 0], X_il[y_il == classe, 1], color=color,
                   edgecolor="k", s=30, label=f"classe {classe}")
    ax.set_xlabel("columna 1 (inventada)")
    ax.grid(alpha=0.3)
x1_il = np.linspace(X_il[:, 0].min(), X_il[:, 0].max(), 50)
ax2.plot(x1_il, -(a1 * x1_il + bb) / a2, "k--", linewidth=2, label="frontera")
ax1.set_ylabel("columna 2 (inventada)")
ax1.set_title("El núvol, pintat per classe")
ax2.set_title(f"Amb la frontera: precisió {model_il.score(X_il, y_il):.1%}")
ax2.set_ylim(X_il[:, 1].min() - 0.5, X_il[:, 1].max() + 0.5)   # que la recta no estiri l'eix
ax1.legend(loc="upper left")
ax2.legend(loc="lower right")
plt.tight_layout()
plt.show()
"""))))


# ------------------------------------------------- correccions de contingut del text original
# (vell, nou): substitucions exactes; si el vell ja no hi es, no fa res.
CORRECCIONS = [
    ("El punt vermell cau ben endins de la zona fosca: el fons de la vall. No és exactament\nel punt més baix de tota la graella",
     "El punt vermell és el mínim que troba scikit-learn, i cau ben endins de la zona fosca. No\nés el punt més baix de tota la graella"),
    ("és el punt vermell de la\nsecció anterior, el fons de la vall que hem trobat provant graella per graella. Nosaltres\nhem trigat una estona provant combinacions; scikit-learn hi arriba en una fracció de\nsegon amb descens de gradient.",
     "és el punt vermell de la\nsecció anterior, el mínim que troba scikit-learn. Nosaltres hem trigat una estona provant\ncombinacions; scikit-learn hi arriba en una fracció de segon amb **L-BFGS**, un mètode de\nla mateixa família que el descens de gradient però més llest: a més del pendent, estima\ncom es corba el paisatge i ajusta la passa a cada direcció. Ho veureu a `MA_02`."),
    ("Per a tres (o més) classes, scikit-learn fa servir l'estratègia\n**un contra la resta** (*one-vs-rest*): entrena **tres** models binaris per sota\n(«és setosa o no?», «és versicolor o no?», «és virginica o no?») i, per a cada flor,\nes queda amb l'espècie que hagi donat la probabilitat més alta.",
     "Per a tres (o més) classes, scikit-learn fa servir la regressió\nlogística **multinomial**: calcula **una $z$ per espècie**, cadascuna amb els seus pesos,\ni les converteix totes alhora en probabilitats amb la funció **softmax**,\n$p_k = e^{z_k} / \\sum_j e^{z_j}$, que és la generalització de la sigmoide a més de dues\nclasses. Les tres probabilitats sumen 1 per construcció, i la flor va a l'espècie amb la\nprobabilitat més alta.\n\nL'alternativa clàssica és **un contra la resta** (*one-vs-rest*): entrenar tres models\nbinaris independents («és setosa o no?», «és versicolor o no?», «és virginica o no?») i\nquedar-se amb el que doni més. scikit-learn ho fa si se li demana amb\n`OneVsRestClassifier` (de `sklearn.multiclass`), però per defecte fa servir la multinomial."),
    ("- Amb l'estratègia **un contra la resta**, la mateixa idea serveix per a més de dues\n  classes.",
     "- Amb la **softmax** (regressió logística multinomial), la mateixa idea serveix per a més\n  de dues classes."),
]


def principal():
    nb = json.load(io.open(QUADERN, encoding="utf-8"))
    cels = [c for c in nb["cells"] if c.get("metadata", {}).get("afegit") != MARCA]
    for c in cels:
        text = "".join(c["source"])
        for vell, nou in CORRECCIONS:
            text = text.replace(vell, nou)
        if text != "".join(c["source"]):
            c["source"] = md(text)["source"]
    for ancora, noves in INSERCIONS:
        trobades = [i for i, c in enumerate(cels) if ancora in "".join(c["source"])]
        if len(trobades) != 1:
            raise SystemExit(f"Ancora {ancora!r}: {len(trobades)} coincidencies (n'esperava 1)")
        i = trobades[0]
        cels[i + 1:i + 1] = noves
    nb["cells"] = cels
    io.open(QUADERN, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
    n_noves = sum(len(n) for _, n in INSERCIONS)
    print(f"{QUADERN}: {len(cels)} cel.les ({n_noves} afegides per aquest script)")


if __name__ == "__main__":
    principal()
