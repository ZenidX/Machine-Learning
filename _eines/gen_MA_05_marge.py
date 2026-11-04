# -*- coding: utf-8 -*-
"""Genera el quadern MA_05: marge, optimitzacio amb restriccions i kernels.

    CEIABD-IA/.venv/Scripts/python.exe _eines/gen_MA_05_marge.py
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu  # noqa: E402

DESTI = "Machine Learning/03_matematiques/MA_05_marge_optimitzacio.ipynb"

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# El marge, l'optimització amb restriccions i d'on surten els kernels

**Optativa d'Aprenentatge automàtic — DAM/DAW 2n — Bloc de matemàtiques**

Fins ara heu minimitzat funcions **lliurement**. Al quadern
`MA_02_descens_gradient.ipynb` vau derivar la log-loss i vau baixar pel
gradient fins al mínim: cap restricció, cap condició, tot el pla obert.

Aquest quadern respon una altra pregunta: **què passa quan la solució ha de
complir condicions?** Quan no val qualsevol punt del pla, només els que
compleixen certes igualtats o desigualtats.

L'SVM és el model del curs on això es veu millor, i no per casualitat:
**tota la forma de l'SVM surt de les restriccions**. Els vectors de suport
no són una optimització d'enginyeria per estalviar memòria; són una
conseqüència matemàtica d'una condició concreta que veurem al punt 5. I el
truc del kernel, que a `ML_05_svm.ipynb` vau veure com una idea intuïtiva
(«busquem una recta en un espai més gran»), aquí surt de mirar on apareixen
les dades dins del problema optimitzat.

Al quadern d'SVM vam deixar dues coses pendents:

1. El marge el vam calcular **amb geometria**, amb la fórmula de la
   distància punt-recta **donada**. Aquí la deduirem.
2. Vam dir «l'SVM resol una optimització, però nosaltres no la resoldrem».
   Aquí hi entrem.

**Avís d'honestedat, per endavant.** No derivarem el problema dual sencer.
És massa llarg per a aquest nivell i no aporta res que no puguem veure d'una
altra manera. El que farem és: presentar el resultat del dual, dir clarament
que no el derivem, i **verificar-lo numèricament** amb un model ja entrenat.
Cada cop que ens saltem un pas, ho direm.
"""))

A(md(r"""
## 0. El que fa falta

Tot el que hi ha aquí funciona amb `numpy`, `pandas`, `matplotlib`,
`scikit-learn` i `scipy`. Res més, i cap fitxer local.
"""))

A(code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_blobs
from sklearn.svm import SVC
from sklearn.metrics.pairwise import rbf_kernel
from scipy.optimize import minimize

np.random.seed(42)
np.set_printoptions(precision=8, suppress=True)

print("numpy", np.__version__)
"""))

# ---------------------------------------------------- 1. distancia punt-recta
A(md(r"""
## 1. La distància d'un punt a una recta, deduïda

Una frontera lineal s'escriu

$$w \cdot x + b = 0$$

on $w$ és el vector de pesos i $b$ el desplaçament. A `ML_05_svm.ipynb` us
vam donar la distància d'un punt $x_0$ a aquesta frontera:

$$d(x_0) = \frac{|w \cdot x_0 + b|}{\|w\|}$$

Ara la deduirem. Tot depèn d'un fet: **$w$ és perpendicular a la frontera.**

### 1.1 Per què $w$ és perpendicular

Agafeu dos punts qualssevol de la frontera, $p$ i $q$. Tots dos la compleixen:

$$w \cdot p + b = 0 \qquad \text{i} \qquad w \cdot q + b = 0$$

Resteu les dues igualtats. Els $b$ es cancel·len i queda

$$w \cdot (p - q) = 0$$

El vector $p - q$ va d'un punt de la recta a un altre punt de la recta: és
un vector **que porta la direcció de la recta**. Si el seu producte escalar
amb $w$ és zero, $w$ és perpendicular a aquesta direcció. I com que això val
per a **qualsevol** parella de punts de la frontera, $w$ és perpendicular a
la frontera sencera.

Comprovem-ho amb números. Fem servir la recta $3x_1 + 4x_2 - 12 = 0$, és a
dir $w = (3, 4)$ i $b = -12$. Dos punts que la compleixen: $(4, 0)$ i
$(0, 3)$.
"""))

A(code(r"""
w_demo = np.array([3.0, 4.0])
b_demo = -12.0

p = np.array([4.0, 0.0])   # 3*4 + 4*0 - 12 = 0
q = np.array([0.0, 3.0])   # 3*0 + 4*3 - 12 = 0

print("p és a la recta?", w_demo @ p + b_demo)
print("q és a la recta?", w_demo @ q + b_demo)

direccio = p - q
print("direcció de la recta (p - q):", direccio)
print("w . (p - q) =", w_demo @ direccio)
"""))

A(md(r"""
El producte escalar surt exactament `0.0`: $w$ i la direcció de la recta són
perpendiculars.

### 1.2 De la perpendicularitat a la distància

Ara la deducció, per projecció. Sigui $x_p$ un punt **qualsevol** de la
frontera i $x_0$ el punt del qual volem la distància. El vector que els
uneix és $x_0 - x_p$.

Aquest vector es pot descompondre en dues parts: una paral·lela a la
frontera i una perpendicular. **La distància a la frontera és la longitud de
la part perpendicular**, perquè la part paral·lela us mou al llarg de la
recta sense acostar-vos-hi ni allunyar-vos-en.

El vector normal unitari és $n = \dfrac{w}{\|w\|}$ (unitari perquè té
longitud 1). La component de $x_0 - x_p$ en la direcció de $n$ és la seva
projecció escalar:

$$(x_0 - x_p) \cdot n = \frac{(x_0 - x_p) \cdot w}{\|w\|}
= \frac{w \cdot x_0 - w \cdot x_p}{\|w\|}$$

I aquí ve el pas que ho tanca tot: $x_p$ és a la frontera, per tant
$w \cdot x_p + b = 0$, és a dir $w \cdot x_p = -b$. Substituïm:

$$(x_0 - x_p) \cdot n = \frac{w \cdot x_0 + b}{\|w\|}$$

Prenem el valor absolut (la distància no té signe) i ja hi som:

$$d(x_0) = \frac{|w \cdot x_0 + b|}{\|w\|}$$

Fixeu-vos en una cosa: **el resultat no depèn de quin $x_p$ hem triat.** Això
és el que fa que la fórmula sigui una distància a la recta i no a un punt
concret d'ella.

Traducció a NumPy, línia per línia:

- $w \cdot x_0 + b$ és `X @ w + b`
- $\|w\|$ és `np.linalg.norm(w)`
- el valor absolut és `np.abs`
"""))

A(code(r"""
def distancia(w, b, X):
    # Distància de cada fila de X a la frontera w . x + b = 0
    return np.abs(X @ w + b) / np.linalg.norm(w)


punts = np.array([
    [0.0, 0.0],   # l'origen
    [4.0, 4.0],
    [1.0, 1.0],
    [4.0, 0.0],   # aquest SÍ que és a la recta: distància 0
])

d = distancia(w_demo, b_demo, punts)
for x0, di in zip(punts, d):
    print(f"punt {x0} -> distància {di:.4f}")
"""))

A(md(r"""
L'origen queda a **2,4** de la recta, $(4,4)$ a **3,2**, $(1,1)$ a **1,0** i
$(4,0)$ a **0** perquè hi és a sobre.

No us cregueu la fórmula perquè estigui escrita. Comprovem-la per força
bruta: generem molts punts de la recta i mirem quin és el més proper a cada
punt.
"""))

A(code(r"""
# Parametritzem la recta: partim de p i ens movem en la seva direcció.
u = (p - q) / np.linalg.norm(p - q)          # direcció unitària de la recta
t = np.linspace(-20, 20, 400001)
linia = p + t[:, None] * u                   # 400.001 punts de la recta

for x0 in [np.array([0.0, 0.0]), np.array([4.0, 4.0]), np.array([1.0, 1.0])]:
    forca_bruta = np.linalg.norm(linia - x0, axis=1).min()
    formula = distancia(w_demo, b_demo, x0[None, :])[0]
    print(f"punt {x0}:  força bruta = {forca_bruta:.6f}   fórmula = {formula:.6f}"
          f"   diferència = {abs(forca_bruta - formula):.2e}")
"""))

A(md(r"""
Les diferències són **0** per als dos primers punts i
$3{,}33 \cdot 10^{-16}$ per al tercer, que és error d'arrodoniment de la coma
flotant. La fórmula no és un conveni: és la distància de veritat.
"""))

A(code(r"""
plt.figure(figsize=(7, 6))

x1 = np.linspace(-1, 6, 100)
x2 = (-b_demo - w_demo[0] * x1) / w_demo[1]
plt.plot(x1, x2, color="black", label=r"recta $3x_1 + 4x_2 - 12 = 0$")

for x0, di in zip(punts, d):
    plt.scatter(*x0, s=70, zorder=5, color="tab:blue")
    # peu de la perpendicular: x0 menys la component normal
    normal = w_demo / np.linalg.norm(w_demo)
    signe = np.sign(w_demo @ x0 + b_demo)
    peu = x0 - signe * di * normal
    plt.plot([x0[0], peu[0]], [x0[1], peu[1]], "--", color="tab:red", alpha=0.7)
    plt.annotate(f"d={di:.2f}", x0 + np.array([0.12, 0.12]))

plt.scatter([], [], color="tab:blue", label="punts mesurats")
plt.plot([], [], "--", color="tab:red", label="distància (perpendicular)")
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.title("La distància a la recta és la perpendicular")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.legend()
plt.show()
"""))

# ------------------------------------------------- 2. el marge i l'escalat
A(md(r"""
## 2. El marge i l'escalat que sembla trampa

El marge d'una frontera és la distància al punt més proper, per les dues
bandes. A `ML_05_svm.ipynb` el vam calcular directament amb la fórmula del
punt 1. Als llibres, en canvi, sempre el veureu escrit així:

$$\text{marge} = \frac{2}{\|w\|}$$

Aquesta expressió només és certa si **s'imposa** que els punts més propers a
la frontera compleixin

$$|w \cdot x_i + b| = 1$$

I aquí és on l'alumne desconfiat aixeca la mà: *d'on surt aquest 1? Qui diu
que els punts més propers valguin exactament 1?*

### 2.1 Per què la normalització no perd generalitat

Ningú ho diu. **Ho decidim nosaltres**, i podem fer-ho perquè la frontera
$w \cdot x + b = 0$ i la frontera $(cw) \cdot x + (cb) = 0$ **són la mateixa
recta** per a qualsevol $c > 0$. Multiplicar per $c$ no mou res:

$$cw \cdot x + cb = c\,(w \cdot x + b)$$

Si $w \cdot x + b$ era zero, $c$ vegades zero segueix sent zero. Si era
positiu, segueix sent positiu. La recta, les prediccions i les distàncies
**no canvien**. L'únic que canvia és l'escala dels números: $\|cw\| =
c\|w\|$, i el valor de $w \cdot x + b$ per a cada punt es multiplica per $c$.

Aquesta llibertat és una **redundància** del model: hi ha infinites parelles
$(w, b)$ que descriuen la mateixa frontera. Per treure-la, fixem l'escala:
exigim que el punt més proper doni exactament 1. Això tria una parella
concreta de totes les infinites possibles, i a canvi la fórmula del marge
queda neta.

Si el punt més proper compleix $|w \cdot x_i + b| = 1$, la seva distància és
$1/\|w\|$. Com que hi ha punts a les dues bandes, l'amplada total de la
banda buida és $2/\|w\|$.

Comprovem l'escalat amb la recta C del quadern d'SVM: $w = (1, 1)$,
$b = -3{,}2$, sobre les mateixes dades d'Iris.
"""))

A(code(r"""
iris = load_iris(as_frame=True)
dades = iris.frame.copy()
dades["especie"] = iris.target_names[iris.target]
dades = dades.rename(columns={
    "sepal length (cm)": "sepal_llarg",
    "sepal width (cm)": "sepal_ample",
    "petal length (cm)": "petal_llarg",
    "petal width (cm)": "petal_ample",
})

dos = dades[dades["especie"].isin(["setosa", "versicolor"])].reset_index(drop=True)
X = dos[["petal_llarg", "petal_ample"]].to_numpy()
y = (dos["especie"] == "versicolor").to_numpy().astype(int)

print("Mostres:", X.shape, " setosa:", (y == 0).sum(), " versicolor:", (y == 1).sum())
"""))

A(code(r"""
w_c = np.array([1.0, 1.0])
b_c = -3.2

c = 5.0
w_gran, b_gran = c * w_c, c * b_c

print(f"||w||     = {np.linalg.norm(w_c):.6f}")
print(f"||5w||    = {np.linalg.norm(w_gran):.6f}   (5 vegades més gran)")
print()

# 1) la frontera: quins punts la compleixen
print("valors de w.x+b als 3 primers punts:      ", (X @ w_c + b_c)[:3])
print("valors de 5w.x+5b als mateixos 3 punts:   ", (X @ w_gran + b_gran)[:3])
print("  -> els segons són exactament 5 vegades els primers")
print()

# 2) les prediccions: només depenen del signe
pred_original = np.sign(X @ w_c + b_c)
pred_escalada = np.sign(X @ w_gran + b_gran)
print("prediccions idèntiques?", np.array_equal(pred_original, pred_escalada))

# 3) les distàncies: la norma del denominador compensa l'escalat
d_original = distancia(w_c, b_c, X)
d_escalada = distancia(w_gran, b_gran, X)
print("màxima diferència entre distàncies:", np.abs(d_original - d_escalada).max())
print(f"marge geomètric (mínim de les distàncies): {d_original.min():.6f}")
"""))

A(md(r"""
Els números ho diuen tot:

- $\|w\| = 1{,}414214$ i $\|5w\| = 7{,}071068$: la norma **sí** que canvia.
- Els valors de $w \cdot x + b$ es multipliquen per 5 exactament.
- Les prediccions són **idèntiques** (`True`).
- Les distàncies coincideixen amb una diferència màxima de
  $8{,}88 \cdot 10^{-16}$, que és zero en aritmètica de coma flotant.
- El marge geomètric és **0,636396** en tots dos casos.

O sigui: $\|w\|$ tot sol no vol dir res sobre el marge. **Només vol dir
alguna cosa un cop hem fixat l'escala.** Fem-ho ara: dividim $w$ i $b$ pel
valor de $|w \cdot x + b|$ del punt més proper, i mirem si surt
$2/\|w\| = 2 \times 0{,}636396$.
"""))

A(code(r"""
minim_funcional = np.abs(X @ w_c + b_c).min()
print(f"valor de |w.x+b| al punt més proper: {minim_funcional:.6f}")

w_norm = w_c / minim_funcional
b_norm = b_c / minim_funcional
print(f"|w_norm.x+b_norm| al punt més proper: {np.abs(X @ w_norm + b_norm).min():.6f}")
print()
print(f"2/||w_norm||               = {2 / np.linalg.norm(w_norm):.6f}")
print(f"2 x marge geomètric        = {2 * d_original.min():.6f}")
print(f"mateixes prediccions que abans?  "
      f"{np.array_equal(np.sign(X @ w_norm + b_norm), pred_original)}")
"""))

A(md(r"""
Amb la normalització imposada, $2/\|w\| = 1{,}272792$, que és exactament el
doble del marge geomètric $0{,}636396$. I les prediccions són les mateixes
que abans: la frontera no s'ha mogut, només hem triat una escala.

El valor de $|w \cdot x + b|$ al punt més proper era **0,900000**; dividint
$w$ i $b$ per 0,9 passa a ser **1,000000** exacte, que és el que volíem
imposar.

**La fórmula $2/\|w\|$ no és la fórmula del marge: és la fórmula del marge
sota una normalització concreta.** Si algú us la dóna sense dir-ho, us està
amagant un pas.

Dibuixat. Als tres panells la frontera negra és **la mateixa recta**. El que canvia són
les dues rectes discontínues, on $w \cdot x + b = +1$ i $w \cdot x + b = -1$: depenen de
l'escala. Només amb la normalització passen just pels punts més propers, i només llavors
la franja entre elles és el carrer buit i fa $2/\|w\|$ d'ample.
"""))

A(code(r"""
fig, axs = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
g1, g2 = np.meshgrid(np.linspace(0.5, 5.5, 300), np.linspace(-0.1, 2.0, 300))
casos = [(w_c, b_c, "(w, b) de la recta C"),
         (w_gran, b_gran, "(5w, 5b): mateixa recta"),
         (w_norm, b_norm, "normalitzada: el punt més proper dona 1")]
for ax, (ww, bb, titol) in zip(axs, casos):
    valor = g1 * ww[0] + g2 * ww[1] + bb
    ax.contourf(g1, g2, valor, levels=[-1, 1], colors=["gold"], alpha=0.35)
    ax.contour(g1, g2, valor, levels=[-1, 0, 1], colors="k", linestyles=["--", "-", "--"])
    ax.scatter(X[y == 0, 0], X[y == 0, 1], color="tab:blue", edgecolor="k", s=20)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], color="tab:orange", edgecolor="k", s=20)
    a_prop = np.argsort(np.abs(X @ ww + bb))[:2]       # els dos punts més propers
    ax.scatter(X[a_prop, 0], X[a_prop, 1], s=180, facecolors="none",
               edgecolors="tab:red", linewidths=2)
    ax.set_title(f"{titol}\n$2/\\|w\\|$ = {2 / np.linalg.norm(ww):.3f}")
    ax.set_xlabel("llargada del pètal")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("amplada del pètal")
fig.suptitle("La frontera no es mou; les rectes $w \\cdot x + b = \\pm 1$ sí "
             "(cercles vermells: els punts més propers)")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
A l'esquerra la franja és més ampla que el buit (els punts més propers hi queden a
dins) i al mig és molt més estreta. Cap de les dues és el marge. A la dreta les rectes
discontínues toquen els cercles vermells: ara sí, $2/\|w\| = 1{,}273$ és l'amplada del
carrer.
"""))

# ------------------------------------------------- 3. plantejament formal
A(md(r"""
## 3. El plantejament formal

Ara ja podem escriure el problema de l'SVM tal com es planteja de veritat.

Volem **maximitzar** el marge $2/\|w\|$. Maximitzar una fracció amb
numerador constant és minimitzar el denominador, i minimitzar $\|w\|$ és el
mateix que minimitzar $\frac{1}{2}\|w\|^2$ (elevar al quadrat no canvia
l'ordre entre números positius; el $\frac{1}{2}$ hi és perquè en derivar es
cancel·la amb el 2 de l'exponent i queda més net).

$$\boxed{\;\min_{w,\,b} \; \frac{1}{2}\|w\|^2
\qquad \text{subjecte a} \qquad
y_i\,(w \cdot x_i + b) \ge 1 \quad \text{per a tota } i \;}$$

**Fixeu-vos en la inversió, que és el pas que despista més:** el que volem és
un marge **gran**, i el que escrivim és un **mínim** de la norma dels pesos.
No és una casualitat ni un truc de notació: com més petit és $\|w\|$, més
ampla és la banda $2/\|w\|$. Un $w$ gran vol dir una frontera que canvia de
valor molt de pressa quan et mous, i per tant una banda estreta.

### Què vol dir cada restricció, en paraules

Hi ha una restricció per cada mostra d'entrenament. Aquí $y_i$ val $+1$ o
$-1$ (no 0 i 1 com a `scikit-learn`; ara veureu per què).

$$y_i\,(w \cdot x_i + b) \ge 1$$

- Si la mostra $i$ és de la classe positiva ($y_i = +1$), la restricció diu
  $w \cdot x_i + b \ge 1$: **queda't a la banda positiva, i com a mínim a
  distància 1 de la frontera** (en unitats funcionals, no geomètriques).
- Si és de la classe negativa ($y_i = -1$), multiplicar per $-1$ gira la
  desigualtat: $w \cdot x_i + b \le -1$. **Queda't a la banda negativa, i com
  a mínim a distància 1.**

Multiplicar per $y_i$ és el que permet escriure les dues condicions amb una
sola línia. El producte $y_i(w \cdot x_i + b)$ és positiu quan el model
encerta i negatiu quan s'equivoca; se'n diu el **marge funcional** de la
mostra $i$.

En paraules planes, el problema sencer diu: **estreny $w$ tant com puguis,
però sense que cap punt se't fiqui dins de la banda.**

Aquest és el primer problema d'optimització del curs amb restriccions. El
descens de gradient de `MA_02_descens_gradient.ipynb` no serveix tal qual: si
baixeu pel gradient de $\frac{1}{2}\|w\|^2$ arribareu a $w = 0$, que té marge
infinit i no separa res. **El gradient no sap que hi ha restriccions.** Ens
fa falta una eina que les tingui en compte.
"""))

# ------------------------------------------------- 4. multiplicadors de Lagrange
A(md(r"""
## 4. Multiplicadors de Lagrange, des de zero

No comencem per l'SVM. Comencem pel problema amb restriccions més petit que
es pot escriure:

$$\min_{x,y} \; f(x, y) = x^2 + y^2
\qquad \text{subjecte a} \qquad g(x, y) = x + y - 1 = 0$$

En paraules: **de tots els punts de la recta $x + y = 1$, quin és el més a
prop de l'origen?** Sense la restricció la resposta seria $(0, 0)$, però
$(0,0)$ no és a la recta i per tant no val.

La resposta, per simetria, hauria de ser $(0{,}5,\ 0{,}5)$. Ho resoldrem de
tres maneres independents per comprovar-ho.

### 4.1 Manera (a): substituir la restricció i derivar

Si $x + y = 1$, aleshores $y = 1 - x$. Substituïm dins de $f$ i ens quedem
amb una funció d'una sola variable, **sense restriccions**:

$$h(x) = x^2 + (1-x)^2 = x^2 + 1 - 2x + x^2 = 2x^2 - 2x + 1$$

Derivem i igualem a zero, com sempre:

$$h'(x) = 4x - 2 = 0 \;\Longrightarrow\; x = \frac{1}{2}
\;\Longrightarrow\; y = 1 - \frac{1}{2} = \frac{1}{2}$$

La segona derivada és $h''(x) = 4 > 0$, per tant és un mínim i no un màxim.
"""))

A(code(r"""
def f_obj(v):
    # f(x, y) = x^2 + y^2
    return v[0] ** 2 + v[1] ** 2


def h(x):
    # f amb la restricció y = 1 - x ja substituïda
    return 2 * x ** 2 - 2 * x + 1


x_sub = 2 / 4           # de h'(x) = 4x - 2 = 0
sol_a = np.array([x_sub, 1 - x_sub])
print("(a) substitució:", sol_a, " f =", f_obj(sol_a))

# comprovació grollera: cap punt de la recta ha de donar un f més petit
xs = np.linspace(-2, 3, 500001)
fs = h(xs)
print("    mínim numèric de h sobre la recta:", xs[fs.argmin()], fs.min())
"""))

A(md(r"""
### 4.2 Manera (b): el lagrangià

La substitució ha funcionat perquè la restricció era fàcil d'aïllar. Amb cent
restriccions i vint variables no es podrà. El mètode general és el
**lagrangià**: es construeix una funció nova que junta l'objectiu i la
restricció amb una variable extra $\lambda$, el **multiplicador**:

$$\mathcal{L}(x, y, \lambda) = f(x, y) - \lambda\, g(x, y)
= x^2 + y^2 - \lambda\,(x + y - 1)$$

I després es busca on totes les derivades parcials són zero, **també la de
$\lambda$**:

$$\frac{\partial \mathcal{L}}{\partial x} = 2x - \lambda = 0$$
$$\frac{\partial \mathcal{L}}{\partial y} = 2y - \lambda = 0$$
$$\frac{\partial \mathcal{L}}{\partial \lambda} = -(x + y - 1) = 0$$

La tercera equació **és** la restricció: derivar respecte de $\lambda$ la
torna a treure. Això és l'elegància del mètode: la restricció deixa de ser
una condició externa i passa a ser una equació més del sistema.

Les dues primeres es poden llegir juntes com

$$\nabla f = \lambda \nabla g$$

és a dir: **al punt òptim, el gradient de l'objectiu i el gradient de la
restricció apunten en la mateixa direcció** (poden diferir en la longitud, i
d'això se n'encarrega $\lambda$). Al punt 4.4 veureu què vol dir això
geomètricament.

En aquest cas les tres equacions són lineals, així que el sistema es pot
escriure en forma matricial i resoldre amb `np.linalg.solve`:

$$\begin{pmatrix} 2 & 0 & -1 \\ 0 & 2 & -1 \\ 1 & 1 & 0 \end{pmatrix}
\begin{pmatrix} x \\ y \\ \lambda \end{pmatrix} =
\begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$
"""))

A(code(r"""
# files: dL/dx = 0, dL/dy = 0, restricció x + y = 1
A_sist = np.array([
    [2.0, 0.0, -1.0],
    [0.0, 2.0, -1.0],
    [1.0, 1.0,  0.0],
])
b_sist = np.array([0.0, 0.0, 1.0])

x_lag, y_lag, lambda_lag = np.linalg.solve(A_sist, b_sist)
sol_b = np.array([x_lag, y_lag])
print("(b) lagrangià:", sol_b, " lambda =", lambda_lag, " f =", f_obj(sol_b))

# els dos gradients al punt òptim
grad_f = np.array([2 * x_lag, 2 * y_lag])
grad_g = np.array([1.0, 1.0])
print("   grad f        =", grad_f)
print("   lambda grad g =", lambda_lag * grad_g)
print("   són iguals?", np.allclose(grad_f, lambda_lag * grad_g))
"""))

A(md(r"""
Surt $(0{,}5,\ 0{,}5)$ amb $\lambda = 1$, i els dos gradients coincideixen:
$\nabla f = (1, 1)$ i $\lambda \nabla g = 1 \cdot (1, 1) = (1, 1)$.

### 4.3 Manera (c): numèricament, amb `scipy`

`scipy.optimize.minimize` accepta un argument `constraints`. Cada restricció
és un diccionari amb `"type"` (`"eq"` per igualtat, `"ineq"` per desigualtat
$\ge 0$) i `"fun"`, la funció que ha de valer zero (o ser positiva).
L'optimitzador no sap res de lagrangians ni de la nostra deducció: busca pel
seu compte.
"""))

A(code(r"""
restriccio = {"type": "eq", "fun": lambda v: v[0] + v[1] - 1}

res = minimize(f_obj, x0=np.array([2.0, -3.0]), constraints=[restriccio])
sol_c = res.x
print("(c) scipy:", sol_c, " f =", res.fun, " ha convergit?", res.success)
print()
print("--- les tres solucions ---")
print("(a) substitució :", sol_a)
print("(b) lagrangià   :", sol_b)
print("(c) scipy       :", sol_c)
print()
print("(a) vs (b) coincideixen?", np.allclose(sol_a, sol_b))
print("(a) vs (c) coincideixen (tolerància 1e-3)?", np.allclose(sol_a, sol_c, atol=1e-3))
print("diferència màxima (a) vs (c):", np.abs(sol_a - sol_c).max())
"""))

A(md(r"""
Les tres donen $(0{,}5,\ 0{,}5)$. La de `scipy` amb una desviació de
$4{,}8 \cdot 10^{-4}$, que és el que s'espera d'un mètode numèric iteratiu
amb la seva tolerància per defecte; les dues analítiques són exactes.

### 4.4 Què vol dir $\nabla f = \lambda \nabla g$, geomètricament

El gràfic que ve és el més important d'aquesta secció. Dibuixem les **corbes
de nivell** de $f$ (cercles, perquè $x^2+y^2$ és constant a distància
constant de l'origen) i a sobre la recta de la restricció.

Penseu-hi com un passeig: camineu per la recta i aneu creuant cercles. Cada
cercle que creueu és un valor de $f$. Mentre **creueu** cercles, esteu
canviant el valor de $f$, així que no podeu ser al mínim: sempre hi ha un
cercle més petit a l'abast. Al punt on ja no creueu cap cercle sinó que el
**toqueu** (la recta és tangent), $f$ ha deixat d'empitjorar i de millorar:
aquell és l'òptim.

I la tangència és exactament $\nabla f = \lambda \nabla g$: el gradient de
$f$ és perpendicular a les seves corbes de nivell, el gradient de $g$ és
perpendicular a la recta, i si la recta i la corba de nivell són tangents,
les dues perpendiculars van en la mateixa direcció.
"""))

A(code(r"""
malla = np.linspace(-1.5, 2.0, 400)
xx, yy = np.meshgrid(malla, malla)
zz = xx ** 2 + yy ** 2

plt.figure(figsize=(7.5, 7))
contorn = plt.contour(xx, yy, zz, levels=[0.1, 0.25, 0.5, 1.0, 2.0, 3.5],
                      colors="tab:gray", alpha=0.8)
plt.clabel(contorn, inline=True, fontsize=8, fmt="f=%.2f")

# la corba de nivell que passa per la solució: f = 0.5
plt.contour(xx, yy, zz, levels=[f_obj(sol_b)], colors="tab:blue", linewidths=2)

x_recta = np.linspace(-1.5, 2.0, 100)
plt.plot(x_recta, 1 - x_recta, color="tab:red", linewidth=2,
         label=r"restricció $x + y = 1$")

plt.scatter(*sol_b, s=120, color="black", zorder=5,
            label=f"òptim ({sol_b[0]:.1f}, {sol_b[1]:.1f})")

# els dos gradients al punt òptim
plt.arrow(sol_b[0], sol_b[1], grad_f[0] * 0.4, grad_f[1] * 0.4,
          head_width=0.06, color="tab:green", zorder=6)
plt.annotate(r"$\nabla f$", sol_b + np.array([0.45, 0.30]), color="tab:green")
plt.arrow(sol_b[0], sol_b[1], grad_g[0] * 0.4, grad_g[1] * 0.4,
          head_width=0.06, color="tab:purple", linestyle=":", zorder=6)
plt.annotate(r"$\nabla g$", sol_b + np.array([0.20, 0.50]), color="tab:purple")

plt.plot([], [], color="tab:blue", linewidth=2, label=r"corba de nivell $f=0.5$")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("L'òptim amb restricció és on la recta és tangent a una corba de nivell")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.legend(loc="upper right")
plt.show()
"""))

A(md(r"""
La recta vermella talla els cercles grisos i **toca** el cercle blau
($f = 0{,}5$) en un sol punt: $(0{,}5,\ 0{,}5)$. Les dues fletxes surten del
mateix punt i van en la mateixa direcció, perquè $\lambda = 1$ i en aquest
cas coincideixen fins en la longitud.

Cap cercle més petit que el blau arriba a tocar la recta. Per això
$f = 0{,}5$ és el mínim assolible **dins de la restricció**, tot i que el
mínim de $f$ sense restriccions és 0.

### 4.5 El passeig, punt per punt

Comprovem la frase «només a l'òptim els gradients són paral·lels». Agafem tres punts de
la recta, calculem $\nabla f = (2x, 2y)$ i $\nabla g = (1, 1)$ a cadascun i mirem si són
paral·lels. Dos vectors del pla són paral·lels quan el seu «producte creuat»
$a_1 b_2 - a_2 b_1$ és zero (és l'àrea del paral·lelogram que formen: zero si estan
alineats).
"""))

A(code(r"""
punts_recta = {"x = -0.3": -0.3, "x = 0.2": 0.2, "x = 0.5 (òptim)": 0.5, "x = 1.1": 1.1}
for nom, xr in punts_recta.items():
    pr = np.array([xr, 1 - xr])
    gf = 2 * pr                                     # gradient de f
    gg = np.array([1.0, 1.0])                       # gradient de g
    creuat = gf[0] * gg[1] - gf[1] * gg[0]
    print(f"{nom:16s}  f = {f_obj(pr):.3f}   grad f = {gf}   creuat = {creuat:+.2f}")
"""))

A(md(r"""
El producte creuat només és zero a $x = 0{,}5$, i és també on $f$ és més petita. Dibuixat:
a l'esquerra, el paisatge de $f$ en 3D i, en vermell, el camí que fa la recta $x + y = 1$
quan la pugem fins a la superfície: una paràbola amb un sol punt més baix. A la dreta,
els gradients als quatre punts: només a l'òptim la fletxa verda ($\nabla f$) i la lila
($\nabla g$) van en la mateixa direcció.
"""))

A(code(r"""
fig = plt.figure(figsize=(15, 6))

ax = fig.add_subplot(1, 2, 1, projection="3d")
s1, s2 = np.meshgrid(np.linspace(-1.2, 1.8, 60), np.linspace(-1.2, 1.8, 60))
ax.plot_surface(s1, s2, s1 ** 2 + s2 ** 2, cmap="viridis", alpha=0.45, linewidth=0)
xr = np.linspace(-0.8, 1.8, 100)
ax.plot(xr, 1 - xr, np.zeros_like(xr), color="tab:red", linestyle="--", label="la recta, a terra")
ax.plot(xr, 1 - xr, xr ** 2 + (1 - xr) ** 2, color="tab:red", linewidth=3,
        label="f al llarg de la recta")
ax.scatter([0.5], [0.5], [0.5], color="black", s=60, depthshade=False, label="òptim")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_zlabel("$f$")
ax.set_title("Pujant la recta fins al paisatge: una paràbola")
ax.view_init(elev=25, azim=-130)
ax.legend(loc="upper left", fontsize=9)

ax2 = fig.add_subplot(1, 2, 2)
ax2.contour(xx, yy, zz, levels=[0.1, 0.25, 0.5, 1.0, 2.0, 3.5], colors="tab:gray", alpha=0.6)
ax2.plot(x_recta, 1 - x_recta, color="tab:red", linewidth=2)
for nom, xr0 in punts_recta.items():
    pr = np.array([xr0, 1 - xr0])
    gf = 2 * pr
    ax2.scatter(*pr, color="black", s=40, zorder=5)
    ax2.annotate("", xy=pr + 0.3 * gf / np.linalg.norm(gf) * 1.5, xytext=pr,
                 arrowprops=dict(arrowstyle="->", color="tab:green", lw=2))
    ax2.annotate("", xy=pr + 0.3 * np.array([1, 1]) / np.sqrt(2) * 1.5, xytext=pr,
                 arrowprops=dict(arrowstyle="->", color="tab:purple", lw=2, linestyle=":"))
ax2.plot([], [], color="tab:green", label=r"$\nabla f$ (direcció)")
ax2.plot([], [], color="tab:purple", linestyle=":", label=r"$\nabla g$ (direcció)")
ax2.set_xlim(-1.2, 2.0)
ax2.set_ylim(-1.2, 2.0)
ax2.set_aspect("equal")
ax2.set_xlabel("$x$")
ax2.set_ylabel("$y$")
ax2.set_title("Només a l'òptim les dues fletxes coincideixen")
ax2.legend(loc="upper right")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

# ---------------------------------- 5. folganca complementaria
A(md(r"""
## 5. La condició que crea els vectors de suport

Al punt 4 la restricció era una **igualtat**: $x + y = 1$, i el punt òptim
l'havia de complir. A l'SVM les restriccions són **desigualtats**:
$y_i(w \cdot x_i + b) \ge 1$. La diferència ho canvia tot.

Amb una desigualtat, cada restricció pot estar en un de dos estats:

- **Activa**: es compleix amb igualtat, $y_i(w \cdot x_i + b) = 1$. El punt
  està justament al límit del que se li permet. Si el moguéssiu una mica cap
  endins, la solució hauria de canviar per fer-li lloc.
- **Inactiva**: es compleix amb marge de sobres,
  $y_i(w \cdot x_i + b) > 1$. El punt és lluny del límit. Podríem esborrar
  aquesta restricció del problema i la solució seria la mateixa.

El lagrangià de l'SVM té un multiplicador $\alpha_i \ge 0$ per cada
restricció:

$$\mathcal{L}(w, b, \alpha) = \frac{1}{2}\|w\|^2
- \sum_i \alpha_i \left[\, y_i(w \cdot x_i + b) - 1 \,\right]$$

I les condicions que ha de complir l'òptim amb desigualtats (se'n diuen
condicions **KKT**, per Karush, Kuhn i Tucker) inclouen una que és la clau de
tot el quadern, la **folgança complementària**:

$$\boxed{\;\alpha_i \left[\, y_i(w \cdot x_i + b) - 1 \,\right] = 0
\quad \text{per a tota } i\;}$$

Llegiu-la a poc a poc. És un producte de dos factors igualat a zero, i sabeu
de batxillerat que un producte és zero quan **almenys un dels dos factors**
és zero. Per tant, per a cada punt $i$, una de dues:

1. $\alpha_i = 0$. El multiplicador és nul. Si mireu el lagrangià, aquest
   punt desapareix del sumatori: **no influeix en la solució**.
2. $y_i(w \cdot x_i + b) - 1 = 0$, és a dir $y_i(w \cdot x_i + b) = 1$. El
   punt està **exactament sobre el marge**.

No hi ha tercera opció. **Un punt, o no compta gens, o està a sobre del
límit.**

Aquest és el resultat que buscàvem. Els punts amb $\alpha_i > 0$ són, per
definició, els **vectors de suport**, i acabem de demostrar que tots ells
estan sobre el marge. Que un SVM depengui només d'uns pocs punts **no és una
optimització d'enginyeria per estalviar memòria, ni una casualitat del
conjunt de dades: és una conseqüència matemàtica de la folgança
complementària.** Surt de la forma del problema, no de la implementació.

### El que ens saltem, dit clarament

No derivarem d'on surt aquest lagrangià ni per què les condicions KKT són
necessàries a l'òptim. Això demana teoria de dualitat i convexitat que no
toca en aquest curs. **Agafem les condicions KKT com un resultat donat i el
verifiquem numèricament.** És el que farem tota l'estona d'aquí endavant: no
demostrem, comprovem.

Comprovem-ho, doncs. Entrenem un `SVC(kernel="linear")` amb un `C` molt gran
sobre les mateixes dades d'Iris del quadern d'SVM. Amb `C` gran el model no
tolera errors, que és exactament el problema del punt 3.
"""))

A(code(r"""
model = SVC(kernel="linear", C=1e5)
model.fit(X, y)

w = model.coef_[0]
b = model.intercept_[0]
print("w =", w)
print("b =", b)
print("2/||w|| =", 2 / np.linalg.norm(w))
print()
print("support_        (índexs dels vectors de suport):", model.support_)
print("support_vectors_ (les mostres):")
print(model.support_vectors_)
print("dual_coef_ (això és alpha_i * y_i, amb signe):", model.dual_coef_)
print()
print("alpha_i (valor absolut de dual_coef_):", np.abs(model.dual_coef_[0]))
print("suma de alpha_i*y_i (ha de ser 0, és una altra condició KKT):",
      model.dual_coef_[0].sum())
"""))

A(md(r"""
Dos vectors de suport de 100 mostres: els índexs 44 i 98.

Ara la comprovació de veritat. Calculem $|w \cdot x_i + b|$ per a **tots** els
punts i separem els vectors de suport de la resta. La folgança complementària
diu que els vectors de suport han de donar exactament 1, i la resta,
estrictament més d'1.
"""))

A(code(r"""
valor_funcional = X @ w + b          # w . x_i + b, per a cada mostra
es_suport = np.zeros(len(X), dtype=bool)
es_suport[model.support_] = True

print("--- VECTORS DE SUPORT (han de donar |w.x+b| = 1) ---")
for i in np.flatnonzero(es_suport):
    posicio = list(model.support_).index(i)
    print(f"  mostra {i:3d}: |w.x+b| = {abs(valor_funcional[i]):.8f}"
          f"   alpha = {abs(model.dual_coef_[0][posicio]):.6f}")

altres = np.flatnonzero(~es_suport)
abs_altres = np.abs(valor_funcional[altres])
print()
print("--- LA RESTA (han de donar |w.x+b| > 1, i alpha = 0) ---")
print(f"  {len(altres)} mostres")
print(f"  mínim   = {abs_altres.min():.8f}")
print(f"  mitjana = {abs_altres.mean():.8f}")
print(f"  màxim   = {abs_altres.max():.8f}")
print(f"  quantes baixen d'1? {(abs_altres < 1).sum()}")
print()
print("Vectors de suport a |w.x+b| = 1 (tolerància 1e-5)?",
      np.allclose(np.abs(valor_funcional[es_suport]), 1.0, atol=1e-5))
print("Tota la resta estrictament per sobre d'1?", (abs_altres > 1).all())
"""))

A(md(r"""
Els números exactes:

- Els dos vectors de suport donen **0,99999987** i **0,99999980**. No són 1
  exacte perquè `libsvm`, la biblioteca que hi ha sota `SVC`, resol el
  problema amb un mètode iteratiu i para quan arriba a la seva tolerància. La
  diferència amb 1 és de l'ordre de $1{,}3 \cdot 10^{-7}$.
- Les 98 mostres restants: el **mínim** és **1,16470573**, la mitjana
  **2,28079195** i el màxim **4,12941106**. **Cap** baixa d'1.

La frontera parteix el pla en tres zones: dins de la banda, res; a la vora
exacta, dos punts; fora, tota la resta. Això és la folgança complementària
feta números.

### La folgança complementària, dibuixada

Primer el cas més petit possible, per veure les dues opcions («o no compta, o és al
límit») sense res més al voltant. El problema del punt 4, però amb una **desigualtat**:
el punt més proper a l'origen **dins** d'un semiplà. Dos casos:

- $x + y \ge 1$: l'origen no hi és, el mínim lliure queda fora. L'òptim s'ha de quedar
  a la vora: la restricció és **activa** i el multiplicador surt positiu.
- $x + y \ge -1$: l'origen ja hi és a dins. L'òptim és el mínim lliure, la restricció no
  fa res: és **inactiva** i el multiplicador és zero.

El multiplicador el traiem igual que al punt 4.2: a l'òptim, $\nabla f = \lambda \nabla g$,
així que $\lambda = \nabla f \cdot \nabla g \,/\, \|\nabla g\|^2$.
"""))

A(code(r"""
fig, axs = plt.subplots(1, 2, figsize=(13, 5.8), sharey=True)
for ax, cte in zip(axs, [1.0, -1.0]):
    restr = {"type": "ineq", "fun": lambda v, c=cte: v[0] + v[1] - c}     # x + y - c >= 0
    opt = minimize(f_obj, x0=np.array([2.0, 2.0]), constraints=[restr]).x
    gf = 2 * opt
    lam = round(gf @ np.array([1.0, 1.0]) / 2.0, 6) + 0.0     # + 0.0: fora el -0.0
    opt = np.round(opt, 6) + 0.0
    activa = abs(opt.sum() - cte) < 1e-6
    print(f"x + y >= {cte:+.0f}:  òptim = {opt}   x + y - c = {opt.sum() - cte:.4f}"
          f"   lambda = {lam:.4f}   ->  {'ACTIVA' if activa else 'inactiva'}")

    ax.contour(xx, yy, zz, levels=[0.1, 0.25, 0.5, 1.0, 2.0, 3.5], colors="tab:gray", alpha=0.6)
    ax.contourf(xx, yy, xx + yy - cte, levels=[0, 100], colors=["tab:green"], alpha=0.12)
    ax.plot(x_recta, cte - x_recta, color="tab:red", linewidth=2, label=f"vora: $x + y = {cte:.0f}$")
    ax.scatter(0, 0, marker="+", color="black", s=120, label="mínim lliure (0, 0)")
    ax.scatter(*opt, s=120, color="black", zorder=5, label=f"òptim, $\\lambda$ = {lam:.2f}")
    ax.set_xlim(-1.5, 2.0)
    ax.set_ylim(-1.5, 2.0)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_title(f"$x + y \\geq {cte:.0f}$: restricció " + ("activa" if activa else "inactiva"))
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)
axs[0].set_ylabel("$y$")
fig.suptitle("Zona verda: on es permet estar. O l'òptim és a la vora, o el multiplicador és 0")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
A l'esquerra, l'òptim és $(0{,}5,\ 0{,}5)$, enganxat a la vora, amb $\lambda = 1$. A la
dreta, l'òptim és l'origen, lluny de la vora, amb $\lambda = 0$: si esborréssiu la
restricció, la resposta seria la mateixa.

L'SVM té una restricció com aquesta **per cada mostra**. Ara posem els cent multiplicadors
d'Iris en un sol gràfic: per a cada mostra, a l'eix horitzontal el seu marge funcional
$y_i(w \cdot x_i + b)$ i al vertical la seva $\alpha_i$. La folgança complementària diu
que cap punt pot tenir les dues coses alhora: $\alpha_i > 0$ i marge $> 1$.
"""))

A(code(r"""
ys = 2 * y - 1                                    # de {0, 1} a {-1, +1}
marge_funcional = ys * (X @ w + b)
alpha = np.zeros(len(X))
alpha[model.support_] = np.abs(model.dual_coef_[0])

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.scatter(marge_funcional[alpha == 0], alpha[alpha == 0], color="tab:blue", s=30, alpha=0.6,
           label=f"{(alpha == 0).sum()} mostres amb $\\alpha_i = 0$")
ax.scatter(marge_funcional[alpha > 0], alpha[alpha > 0], color="tab:red", s=120, edgecolor="k",
           zorder=3, label=f"{(alpha > 0).sum()} vectors de suport ($\\alpha_i > 0$)")
ax.axvline(1, color="black", linestyle="--", linewidth=1)
ax.annotate("marge funcional = 1\n(la vora del carrer)", (1.05, alpha.max() * 0.6))
ax.set_xlabel("$y_i\\,(w \\cdot x_i + b)$, el marge funcional de cada mostra")
ax.set_ylabel("$\\alpha_i$")
ax.set_title("O $\\alpha_i = 0$, o la mostra és just a la vora: mai les dues coses alhora")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
plt.show()
"""))

A(md(r"""
Dues columnes i res més: la fila de baix (tots els $\alpha_i = 0$, escampats per marges
de 1,16 en amunt) i els dos punts vermells clavats a marge 1. El quadrant de dalt a la
dreta, $\alpha_i > 0$ amb marge $> 1$, és buit. Aquesta és la forma de la folgança
complementària.

### La mateixa idea, al pla dels pesos

Un últim dibuix que ho lliga tot amb el punt 4. Fixem $b$ al valor que ha trobat l'SVM i
mirem el problema com a funció només de $(w_1, w_2)$. Llavors:

- L'objectiu $\frac{1}{2}\|w\|^2$ té corbes de nivell circulars centrades a l'origen,
  com la $f$ del punt 4.
- Cada mostra posa una restricció $y_i(w_1 x_{i1} + w_2 x_{i2} + b) \ge 1$, que en aquest
  pla és **una recta** amb un costat permès.
- La zona permesa (verda) és on es compleixen totes alhora.

Amb les cent flors d'Iris hi hauria cent rectes tan juntes que no s'hi veuria res; ho
fem amb deu punts inventats. L'òptim és el punt de la zona verda més proper a l'origen.
Mireu quines rectes toca.
"""))

A(code(r"""
rng = np.random.default_rng(2)
X8 = np.vstack([rng.normal([-1.2, -0.8], 0.5, (5, 2)), rng.normal([1.0, 1.2], 0.5, (5, 2))])
y8 = np.array([0] * 5 + [1] * 5)
ys8 = 2 * y8 - 1
m8 = SVC(kernel="linear", C=1e5).fit(X8, y8)
w8, b8 = m8.coef_[0], m8.intercept_[0]
alpha8 = np.zeros(len(X8))
alpha8[m8.support_] = np.abs(m8.dual_coef_[0])

fig, axs = plt.subplots(1, 2, figsize=(14, 6.5))

# esquerra: les dades, com sempre
ax = axs[0]
g1, g2 = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-3, 3, 300))
valor = m8.decision_function(np.c_[g1.ravel(), g2.ravel()]).reshape(g1.shape)
ax.contourf(g1, g2, valor, levels=[-1, 1], colors=["gold"], alpha=0.35)
ax.contour(g1, g2, valor, levels=[-1, 0, 1], colors="k", linestyles=["--", "-", "--"])
ax.scatter(X8[y8 == 0, 0], X8[y8 == 0, 1], color="tab:blue", edgecolor="k", s=50)
ax.scatter(X8[y8 == 1, 0], X8[y8 == 1, 1], color="tab:orange", edgecolor="k", s=50)
for i, (xi, a) in enumerate(zip(X8, alpha8)):
    ax.annotate(str(i), xi + np.array([0.08, 0.08]), color="tab:red" if a > 0 else "tab:gray")
ax.scatter(*X8[alpha8 > 0].T, s=220, facecolors="none", edgecolors="tab:red", linewidths=2)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title("Les dades: deu punts inventats i el seu carrer")
ax.grid(alpha=0.3)

# dreta: el problema al pla dels pesos, amb b fix
ax = axs[1]
v1, v2 = np.meshgrid(np.linspace(-0.5, 3.0, 400), np.linspace(-0.5, 3.0, 400))
permes = np.ones_like(v1, dtype=bool)
for xi, yi in zip(X8, ys8):
    permes &= yi * (v1 * xi[0] + v2 * xi[1] + b8) >= 1
ax.contourf(v1, v2, permes.astype(float), levels=[0.5, 1.5], colors=["tab:green"], alpha=0.15)
ax.contour(v1, v2, 0.5 * (v1 ** 2 + v2 ** 2), levels=8, colors="tab:gray", alpha=0.4)
ax.contour(v1, v2, 0.5 * (v1 ** 2 + v2 ** 2), levels=[0.5 * w8 @ w8], colors="tab:blue", linewidths=2)
w1_l = np.linspace(-0.5, 3.0, 2)
for i, (xi, yi) in enumerate(zip(X8, ys8)):
    w2_l = (1 / yi - b8 - w1_l * xi[0]) / xi[1]      # la recta yi (w . xi + b) = 1
    actiu = alpha8[i] > 0
    ax.plot(w1_l, w2_l, color="tab:red" if actiu else "tab:gray",
            linewidth=2.5 if actiu else 1, alpha=1 if actiu else 0.6)
# w = suma de alpha_i y_i x_i, posades una darrere l'altra
cua = np.zeros(2)
for coef, sv in zip(m8.dual_coef_[0], m8.support_vectors_):
    ax.annotate("", xy=cua + coef * sv, xytext=cua,
                arrowprops=dict(arrowstyle="->", color="tab:purple", lw=3), zorder=6)
    cua = cua + coef * sv
ax.annotate("", xy=w8, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=2))
ax.scatter(*w8, color="black", s=80, zorder=5, label=f"òptim: w = ({w8[0]:.2f}, {w8[1]:.2f})")
ax.plot([], [], color="tab:red", linewidth=2.5, label=f"restriccions actives ({(alpha8 > 0).sum()})")
ax.plot([], [], color="tab:gray", label=f"restriccions inactives ({(alpha8 == 0).sum()})")
ax.plot([], [], color="tab:blue", linewidth=2, label=r"corba de nivell de $\frac{1}{2}\|w\|^2$")
ax.plot([], [], color="tab:purple", label=r"$\alpha_i y_i x_i$, una darrere l'altra")
ax.set_xlim(-0.5, 3.0)
ax.set_ylim(-0.5, 3.0)
ax.set_aspect("equal")
ax.set_xlabel("$w_1$")
ax.set_ylabel("$w_2$")
ax.set_title("Al pla dels pesos ($b$ fix): una recta per mostra")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("alpha_i de cada mostra:", np.round(alpha8, 4))
print("suma de les fletxes liles:", (m8.dual_coef_ @ m8.support_vectors_)[0], "  w =", w8)
"""))

A(md(r"""
L'òptim (el punt negre) és a la cantonada on es creuen les **dues rectes vermelles**, les
restriccions dels dos vectors de suport (els punts 2 i 6 de l'esquerra). Les altres vuit
rectes deixen l'òptim a la zona permesa sense tocar-lo: són restriccions inactives, i per
això els seus $\alpha_i$ valen zero. És el dibuix del punt 4.4 amb més restriccions: allà,
a l'òptim, $\nabla f$ era un múltiple de $\nabla g$; aquí
$\nabla(\frac{1}{2}\|w\|^2) = w$ és una **combinació** dels gradients de les restriccions
actives. Les fletxes liles en són els trossos, posats un darrere l'altre, i arriben just
a la punta de la fletxa negra: $w = \sum \alpha_i y_i x_i$, la fórmula del punt 6.

### No és un artefacte de tenir només dos punts

Amb dos vectors de suport es podria sospitar que hem trobat un cas
degenerat. Repetim-ho amb dues columnes diferents de la mateixa Iris, els
sèpals, on les classes se separen pitjor i calen més punts per aguantar la
frontera.
"""))

A(code(r"""
X_sepal = dos[["sepal_llarg", "sepal_ample"]].to_numpy()

model_sepal = SVC(kernel="linear", C=1e5)
model_sepal.fit(X_sepal, y)

w_s = model_sepal.coef_[0]
b_s = model_sepal.intercept_[0]
f_s = X_sepal @ w_s + b_s

sup = model_sepal.support_
altres_s = np.setdiff1d(np.arange(len(X_sepal)), sup)

print(f"vectors de suport: {len(sup)} de {len(X_sepal)}  ->  índexs {sup}")
print("alpha_i:", np.abs(model_sepal.dual_coef_[0]))
print("|w.x+b| als vectors de suport:", np.abs(f_s[sup]))
print()
print(f"la resta ({len(altres_s)} mostres): mínim = {np.abs(f_s[altres_s]).min():.8f}"
      f"   mitjana = {np.abs(f_s[altres_s]).mean():.8f}"
      f"   màxim = {np.abs(f_s[altres_s]).max():.8f}")
print("quantes baixen d'1?", (np.abs(f_s[altres_s]) < 1).sum())
"""))

A(md(r"""
Quatre vectors de suport aquesta vegada, i els quatre donen **1,00031**
(mateixa tolerància numèrica de `libsvm`). Les 96 mostres restants tenen un
mínim d'**1,10561120** i una mitjana de **4,82278757**. Els $\alpha_i$ són
molt més grans (entre 15 i 19 en comptes d'1,18), perquè el marge és molt més
estret: $\|w\|$ ha de ser gran i els multiplicadors l'acompanyen.

Dos punts o quatre punts, la condició es compleix igual. No és el conjunt de
dades: és l'estructura del problema.
"""))

# ---------------------------------- 6. reconstruir w
A(md(r"""
## 6. Reconstruir $w$ a partir dels multiplicadors

Si deriveu el lagrangià de l'SVM respecte de $w$ i igualeu a zero (això sí
que ho podeu fer amb el que sabeu de `MA_02_descens_gradient.ipynb`), surt

$$\frac{\partial \mathcal{L}}{\partial w} = w - \sum_i \alpha_i y_i x_i = 0
\qquad \Longrightarrow \qquad
\boxed{\;w = \sum_i \alpha_i y_i x_i\;}$$

Aquesta sí que la podem justificar sense trampa: el primer terme del
lagrangià és $\frac{1}{2}\|w\|^2 = \frac{1}{2}\, w \cdot w$, i la seva
derivada respecte de $w$ és $w$; el segon terme conté
$-\alpha_i y_i (w \cdot x_i)$, i la seva derivada respecte de $w$ és
$-\alpha_i y_i x_i$.

I ara sumeu-hi el que sabeu del punt 5: per a la majoria de punts
$\alpha_i = 0$. Per tant el sumatori només recull els vectors de suport:

$$w = \sum_{i \in \text{suport}} \alpha_i y_i x_i$$

**$w$ és una combinació lineal dels vectors de suport, i de res més.** Les
altres mostres no hi surten. Això tanca el que a `ML_05_svm.ipynb` vau
comprovar esborrant 40 flors i veient que la frontera no es movia: allà ho
vau veure passar, aquí en teniu la fórmula.

A `scikit-learn` els $\alpha_i y_i$ ja venen multiplicats i amb signe dins de
`dual_coef_`, així que el sumatori és un producte de matrius:
`dual_coef_ @ support_vectors_`.
"""))

A(code(r"""
# dual_coef_ ja és alpha_i * y_i (amb signe), de forma (1, n_suport)
w_reconstruit = (model.dual_coef_ @ model.support_vectors_)[0]

print("w reconstruït a mà   :", w_reconstruit)
print("coef_ de scikit-learn:", model.coef_[0])
print()
print("diferència component a component:", np.abs(w_reconstruit - model.coef_[0]))
print("diferència màxima               :", np.abs(w_reconstruit - model.coef_[0]).max())
print("np.allclose?", np.allclose(w_reconstruit, model.coef_[0]))
"""))

A(code(r"""
# El mateix amb el model dels sèpals, que té 4 vectors de suport:
# aquí el sumatori té 4 termes i no és trivial.
suma = np.zeros(2)
for alpha_y, x_sv in zip(model_sepal.dual_coef_[0], model_sepal.support_vectors_):
    suma += alpha_y * x_sv
    print(f"  + ({alpha_y:+.8f}) * {x_sv}  ->  parcial {suma}")

print()
print("w reconstruït (bucle explícit):", suma)
print("coef_ de scikit-learn         :", model_sepal.coef_[0])
print("diferència màxima             :", np.abs(suma - model_sepal.coef_[0]).max())
"""))

A(md(r"""
Al primer model la diferència és **0,0 exacta**, no «molt petita»:
`dual_coef_` i `coef_` surten de la mateixa solució i `coef_` és, per dins,
precisament aquest producte de matrius.

Al segon, el del bucle explícit, la diferència és $2{,}13 \cdot 10^{-14}$. No
és que el resultat sigui diferent: **és que l'ordre de les sumes és
diferent.** `dual_coef_ @ support_vectors_` fa el sumatori amb la rutina de
producte de matrius de BLAS, que agrupa els termes d'una altra manera que el
nostre `for`. La suma de nombres en coma flotant no és associativa, i amb
termes de magnitud 80 i 160 que s'han de cancel·lar per deixar un resultat de
magnitud 6, és normal perdre un parell de decimals al final. És el mateix
número.

Fixeu-vos en els parcials del bucle: salten amunt i avall (els termes
positius i negatius es compensen) i només al quart terme arriben a
$(6{,}31777572,\ -5{,}26481134)$. Els quatre punts hi participen; si en
traieu un, $w$ canvia.
"""))

# ---------------------------------- 7. kernel polinomic
A(md(r"""
## 7. El kernel, ara sí formalment

Aquí ve el segon resultat del dual que agafem donat. Si se substitueix
$w = \sum_i \alpha_i y_i x_i$ dins del lagrangià i s'eliminen $w$ i $b$, el
problema es converteix en un problema en els $\alpha$ sols:

$$\max_{\alpha} \; \sum_i \alpha_i
- \frac{1}{2} \sum_i \sum_j \alpha_i \alpha_j y_i y_j \,(x_i \cdot x_j)
\qquad \text{amb} \quad \alpha_i \ge 0, \quad \sum_i \alpha_i y_i = 0$$

Aquest és el **problema dual**. **No el derivarem.** La substitució i la
manipulació algebraica són mitja pàgina de càlcul que no ensenya res de nou;
el que sí que importa, i es veu de seguida, és **on han anat a parar les
dades**.

Mireu l'expressió i busqueu les $x$. Només surten en un lloc:

$$x_i \cdot x_j$$

Un **producte escalar entre parelles de mostres**. Ni les coordenades soltes,
ni les columnes per separat: només productes escalars. Les dades han
desaparegut com a tals i només queda com de semblants són entre elles.

Això obre una porta. Si substituïm aquest producte escalar per una altra
funció $K(x_i, x_j)$ que també sigui un producte escalar, però d'unes
**versions transformades** de les mostres:

$$K(x_i, x_j) = \phi(x_i) \cdot \phi(x_j)$$

aleshores el problema dual que resolem és exactament el problema dual que
resoldríem si haguéssim transformat les dades amb $\phi$ i després les
haguéssim passat a un SVM lineal. **Però mai no calculem $\phi(x)$.**

### La demostració explícita

No us ho cregueu. Ho comprovarem en un cas on es pot escriure tot. Per a
dades de **dues columnes**, prenem el kernel polinòmic de grau 2:

$$K(a, b) = (a \cdot b)^2$$

i la transformació

$$\phi(x) = \left(x_1^2,\; \sqrt{2}\,x_1 x_2,\; x_2^2\right)$$

que porta un punt de 2 dimensions a un espai de 3. Desenvolupem les dues
bandes a mà.

**Banda esquerra**, el kernel directament:

$$(a \cdot b)^2 = (a_1 b_1 + a_2 b_2)^2
= a_1^2 b_1^2 + 2\,a_1 b_1 a_2 b_2 + a_2^2 b_2^2$$

**Banda dreta**, el producte escalar de les transformacions:

$$\phi(a) \cdot \phi(b)
= a_1^2 \cdot b_1^2
+ \left(\sqrt{2}\,a_1 a_2\right)\left(\sqrt{2}\,b_1 b_2\right)
+ a_2^2 \cdot b_2^2$$
$$= a_1^2 b_1^2 + 2\,a_1 a_2 b_1 b_2 + a_2^2 b_2^2$$

**Són la mateixa expressió.** El terme del mig coincideix perquè
$\sqrt{2} \cdot \sqrt{2} = 2$, i aquest és tot el motiu pel qual el
$\sqrt{2}$ hi és: està posat a propòsit perquè quadri.

Així que el $\sqrt{2}$ no és decoratiu, i la igualtat no és aproximada: és
una identitat algebraica. Comprovem-la amb números.
"""))

A(code(r"""
def phi_poly2(Z):
    # Transformació explícita de 2 columnes a 3: (x1^2, sqrt(2) x1 x2, x2^2)
    return np.column_stack([
        Z[:, 0] ** 2,
        np.sqrt(2) * Z[:, 0] * Z[:, 1],
        Z[:, 1] ** 2,
    ])


def kernel_poly2(A_, B_):
    # K(a, b) = (a . b)^2, parella a parella (files corresponents)
    return np.sum(A_ * B_, axis=1) ** 2


rng = np.random.default_rng(42)
punts_a = rng.normal(size=(5, 2))
punts_b = rng.normal(size=(5, 2))

k_directe = kernel_poly2(punts_a, punts_b)
k_via_phi = np.sum(phi_poly2(punts_a) * phi_poly2(punts_b), axis=1)

print("dimensió original      :", punts_a.shape[1])
print("dimensió després de phi:", phi_poly2(punts_a).shape[1])
print()
for i, (kd, kp) in enumerate(zip(k_directe, k_via_phi)):
    print(f"parella {i}:  K(a,b) = {kd:.12f}   phi(a).phi(b) = {kp:.12f}"
          f"   dif = {abs(kd - kp):.2e}")

print()
print("diferència màxima:", np.abs(k_directe - k_via_phi).max())
print("np.allclose?", np.allclose(k_directe, k_via_phi))
"""))

A(code(r"""
# La mateixa comprovació, però amb la matriu de kernel sencera (5x5):
# totes les parelles contra totes.
K_directe = (punts_a @ punts_b.T) ** 2
K_via_phi = phi_poly2(punts_a) @ phi_poly2(punts_b).T

print("matriu de kernel calculada directament (5x5):")
print(K_directe)
print()
print("diferència màxima amb la via phi:", np.abs(K_directe - K_via_phi).max())
print("np.allclose?", np.allclose(K_directe, K_via_phi))
"""))

A(md(r"""
La diferència màxima parella a parella és **$2{,}64 \cdot 10^{-16}$** i, per a
la matriu sencera, **$1{,}78 \cdot 10^{-15}$**. Això és error d'arrodoniment
de la coma flotant: són el mateix número.

Compteu les operacions. La via de $\phi$ ha calculat 3 coordenades per punt i
després un producte escalar de 3 termes. El kernel ha fet un producte escalar
de 2 termes i l'ha elevat al quadrat: **menys feina, i el mateix resultat.**
Amb grau 2 i 2 columnes la diferència és ridícula; amb grau 5 i 100 columnes,
$\phi$ té 96.560.646 coordenades i el kernel segueix sent un producte escalar
de 100 termes elevat a 5.

**Aquesta és la demostració que el truc del kernel no és màgia.** No hi ha
cap espai ocult ni cap operació misteriosa: hi ha una identitat algebraica
que permet calcular un producte escalar d'un espai gran fent aritmètica a
l'espai petit.

### La identitat, entrenant

L'última comprovació no és d'una fórmula sinó de dos models. Agafem els cercles de
`ML_05_svm.ipynb` (un cercle de punts dins d'un altre) i entrenem:

1. Un SVM **lineal** sobre les dades transformades a mà, $\phi(X)$, en 3D.
2. Un SVM amb `kernel="poly"`, `degree=2`, `gamma=1`, `coef0=0` sobre les dades
   originals, en 2D. Amb aquests paràmetres, el kernel de `scikit-learn` és exactament
   $(a \cdot b)^2$.

Si el truc del kernel és el que diem, els dos models han de ser **el mateix model**.
"""))

A(code(r"""
from sklearn.datasets import make_circles

Xcir, ycir = make_circles(n_samples=200, noise=0.08, factor=0.4, random_state=42)
Phi = phi_poly2(Xcir)

model_phi = SVC(kernel="linear", C=10).fit(Phi, ycir)
model_ker = SVC(kernel="poly", degree=2, gamma=1, coef0=0, C=10).fit(Xcir, ycir)

dec_phi = model_phi.decision_function(Phi)
dec_ker = model_ker.decision_function(Xcir)
print(f"exactitud lineal sobre phi(X): {model_phi.score(Phi, ycir):.1%}")
print(f"exactitud poly sobre X       : {model_ker.score(Xcir, ycir):.1%}")
print("mateixes prediccions?", np.array_equal(model_phi.predict(Phi), model_ker.predict(Xcir)))
print(f"diferència màxima de decision_function: {np.abs(dec_phi - dec_ker).max():.1e}")
"""))

A(md(r"""
Mateixes prediccions, i les dues funcions de decisió coincideixen fins a l'error
d'arrodoniment de la coma flotant. Un model ha construït les tres coordenades; l'altre no les ha vist
mai. Dibuixem el que ha fet el primer: a l'espai de $\phi$ els dos cercles queden
separats per un **pla**. I tornat a 2D, aquest pla és la corba on
$w \cdot \phi(x) + b = 0$, que torna a ser un cercle (una el·lipse, en general).
"""))

A(code(r"""
wp, bp = model_phi.coef_[0], model_phi.intercept_[0]

fig = plt.figure(figsize=(14, 6))
ax = fig.add_subplot(1, 2, 1, projection="3d")
for classe, color in [(0, "tab:blue"), (1, "tab:orange")]:
    sel = ycir == classe
    ax.scatter(Phi[sel, 0], Phi[sel, 1], Phi[sel, 2], color=color, s=12, label=f"classe {classe}")
q1, q2 = np.meshgrid(np.linspace(0, 1.3, 20), np.linspace(-1.0, 1.0, 20))
q3 = (-bp - wp[0] * q1 - wp[1] * q2) / wp[2]
q3[(q3 < 0) | (q3 > 1.3)] = np.nan                  # només el tros que cau dins la caixa
ax.plot_surface(q1, q2, q3, color="tab:green", alpha=0.3)
ax.set_xlabel("$x_1^2$")
ax.set_ylabel("$\\sqrt{2}\\,x_1 x_2$")
ax.set_zlabel("$x_2^2$")
ax.set_zlim(0, 1.3)
ax.set_title("A l'espai de $\\phi$: un pla (verd) separa")
ax.view_init(elev=20, azim=45)
ax.set_box_aspect(None, zoom=0.85)
ax.legend(loc="upper left")

ax2 = fig.add_subplot(1, 2, 2)
r1, r2 = np.meshgrid(np.linspace(-1.4, 1.4, 300), np.linspace(-1.4, 1.4, 300))
Phi_g = phi_poly2(np.c_[r1.ravel(), r2.ravel()])
ax2.contour(r1, r2, (Phi_g @ wp + bp).reshape(r1.shape), levels=[0], colors="tab:green", linewidths=2.5)
ax2.contour(r1, r2, model_ker.decision_function(np.c_[r1.ravel(), r2.ravel()]).reshape(r1.shape),
            levels=[0], colors="black", linestyles=":", linewidths=2)
ax2.scatter(Xcir[ycir == 0, 0], Xcir[ycir == 0, 1], color="tab:blue", s=12)
ax2.scatter(Xcir[ycir == 1, 0], Xcir[ycir == 1, 1], color="tab:orange", s=12)
ax2.plot([], [], color="tab:green", linewidth=2.5, label="el pla de l'esquerra, en 2D")
ax2.plot([], [], color="black", linestyle=":", linewidth=2, label='frontera de kernel="poly"')
ax2.set_aspect("equal")
ax2.set_xlabel("$x_1$")
ax2.set_ylabel("$x_2$")
ax2.set_title("Tornat a 2D: les dues fronteres són la mateixa")
ax2.legend(loc="upper right", fontsize=9)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""))

# ---------------------------------- 8. RBF
A(md(r"""
## 8. El kernel RBF i la dimensió infinita

El kernel que `SVC` fa servir per defecte no és el polinòmic sinó el **RBF**
(*radial basis function*), també anomenat gaussià:

$$K(a, b) = e^{-\gamma \|a - b\|^2}$$

Depèn només de la **distància** entre els dos punts. Si $a = b$ val 1; com
més lluny són, més s'acosta a 0. El paràmetre $\gamma$ diu com de ràpid cau.

### Aquí sí que us hem d'avisar

Per al kernel polinòmic us hem escrit la $\phi$ i l'hem calculada. Per al RBF
**no ho farem, perquè no es pot**: la seva transformació explícita té
**dimensió infinita**.

Es veu si desenvolupeu l'exponencial. Separant el quadrat de la distància:

$$e^{-\gamma\|a-b\|^2}
= e^{-\gamma\|a\|^2} \; e^{-\gamma\|b\|^2} \; e^{2\gamma\,(a \cdot b)}$$

Els dos primers factors depenen d'un sol punt cadascun (són constants
respecte de l'altre). El tercer és l'interessant, i la sèrie de Taylor de
l'exponencial diu

$$e^{2\gamma\,(a \cdot b)} = \sum_{k=0}^{\infty}
\frac{(2\gamma)^k}{k!}\,(a \cdot b)^k$$

Una suma **infinita** de kernels polinòmics, un de cada grau. Cada
$(a \cdot b)^k$ té la seva $\phi$ explícita finita, com la del punt 7, però
n'hi ha infinits. La $\phi$ del RBF és, per tant, una llista infinita de
coordenades.

**I això no és cap problema.** El dual només demana productes escalars, i el
producte escalar el sabem calcular: és una exponencial d'un número. No fa
falta construir l'espai per moure's dins d'ell. El que seria impossible
(escriure infinites coordenades) mai no ens el demanen; el que ens demanen
(el producte escalar) és una línia de codi.

Aquest és el moment del curs on la distinció importa més: **calcular en un
espai** i **construir un espai** no són el mateix.

Comprovem que la nostra implementació coincideix amb la de `scikit-learn`.
"""))

A(code(r"""
def kernel_rbf(A_, B_, gamma):
    # Matriu K[i,j] = exp(-gamma * ||A_[i] - B_[j]||^2), sense bucles
    # A_[:, None, :] - B_[None, :, :] té forma (n_A, n_B, n_columnes)
    dif = A_[:, None, :] - B_[None, :, :]
    dist2 = (dif ** 2).sum(axis=-1)          # ||a - b||^2 per cada parella
    return np.exp(-gamma * dist2)


gamma = 0.5
K_manual = kernel_rbf(punts_a, punts_a, gamma)
K_sklearn = rbf_kernel(punts_a, punts_a, gamma=gamma)

print("matriu de kernel RBF a mà (gamma = 0.5):")
print(K_manual)
print()
print("diferència màxima amb sklearn.metrics.pairwise.rbf_kernel:",
      np.abs(K_manual - K_sklearn).max())
print("np.allclose?", np.allclose(K_manual, K_sklearn))
print()
print("diagonal (K(a,a), ha de ser tot 1):", np.diag(K_manual))
"""))

A(md(r"""
Diferència màxima **$1{,}11 \cdot 10^{-16}$**, i la diagonal és tot uns com
toca: la distància d'un punt a si mateix és zero i $e^0 = 1$.

### Què fa $\gamma$

$\gamma$ controla **l'abast de la influència de cada punt**. Com que
$K(a,b)$ és la «semblança» que el model veu entre dues mostres, un $\gamma$
gran fa que dues mostres es considerin semblants només si són molt a prop.
Dibuixem $K$ com a funció de la distància.
"""))

A(code(r"""
r = np.linspace(0, 4, 300)          # distància entre dos punts

plt.figure(figsize=(8, 5.5))
for g in [0.1, 0.5, 2.0, 10.0]:
    plt.plot(r, np.exp(-g * r ** 2), label=f"gamma = {g}")

plt.axhline(0.5, color="tab:gray", linestyle=":", alpha=0.8)
plt.annotate("semblança 0,5", (3.0, 0.53), color="tab:gray")
plt.xlabel("distància entre els dos punts, $||a-b||$")
plt.ylabel("$K(a,b) = e^{-\\gamma\\,||a-b||^2}$")
plt.title("gamma decideix a quina distància dos punts deixen de semblar-se")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

print("distància a la qual la semblança baixa a 0,5, per cada gamma:")
for g in [0.1, 0.5, 2.0, 10.0]:
    # exp(-g r^2) = 0.5  ->  r = sqrt(ln 2 / g)
    print(f"  gamma = {g:5.1f}  ->  r = {np.sqrt(np.log(2) / g):.4f}")
"""))

A(md(r"""
Amb $\gamma = 0{,}1$ dos punts encara es consideren semblants a mitges a
distància **2,6328**; amb $\gamma = 10$ n'hi ha prou amb **0,2633** per
perdre la meitat de la semblança. Deu vegades més $\gamma$ és una influència
$\sqrt{10}$ vegades més curta.

Això lliga amb el que vau veure a `ML_05_svm.ipynb`: amb `gamma` alt la
frontera s'arruga al voltant de cada mostra, perquè cada mostra només
«parla» amb els seus veïns immediats. Amb `gamma` baix tothom parla amb
tothom i la frontera surt suau.

### La funció de decisió és una suma de campanes

Juntem el punt 6 i el kernel. Si $w = \sum_i \alpha_i y_i \phi(x_i)$, la funció de
decisió en un punt nou $x$ és

$$w \cdot \phi(x) + b = \sum_{i \in \text{suport}} \alpha_i y_i\, K(x_i, x) + b$$

Amb el RBF, cada terme és una **campana** centrada en un vector de suport, amunt o avall
segons la classe, i la funció de decisió n'és la suma. Ho fem en una dimensió perquè es
vegi cada campana: calculem la suma a mà i la comparem amb `decision_function`.
"""))

A(code(r"""
rng = np.random.default_rng(3)
x1d = np.concatenate([rng.normal(-2, 0.8, 15), rng.normal(0.5, 0.6, 15), rng.normal(3, 0.8, 15)])
y1d = np.array([0] * 15 + [1] * 15 + [0] * 15)      # la classe 1 al mig: cap recta la separa
X1d = x1d.reshape(-1, 1)
eix = np.linspace(-5, 6, 600).reshape(-1, 1)

fig, axs = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
for ax, g in zip(axs, [0.3, 5.0]):
    m = SVC(kernel="rbf", gamma=g, C=1).fit(X1d, y1d)
    campanes = m.dual_coef_[0][:, None] * kernel_rbf(m.support_vectors_, eix, g)
    suma_a_ma = campanes.sum(axis=0) + m.intercept_[0]
    print(f"gamma = {g}: {len(m.support_)} vectors de suport, diferència màxima amb "
          f"decision_function = {np.abs(suma_a_ma - m.decision_function(eix)).max():.1e}")

    for c in campanes:
        ax.plot(eix[:, 0], c, color="tab:red" if c.max() > 0 else "tab:blue", alpha=0.35, linewidth=1)
    ax.plot(eix[:, 0], suma_a_ma, color="black", linewidth=2.5, label="suma + b (la funció de decisió)")
    ax.axhline(0, color="tab:gray", linestyle="--")
    ax.scatter(x1d[y1d == 0], np.full((y1d == 0).sum(), -2.6), color="tab:blue", s=25, label="classe 0")
    ax.scatter(x1d[y1d == 1], np.full((y1d == 1).sum(), -2.6), color="tab:orange", s=25, label="classe 1")
    ax.set_ylim(-2.9, 2.9)
    ax.set_xlabel("$x$")
    ax.set_title(f"gamma = {g}: {len(m.support_)} campanes (una per vector de suport)")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("valor")
axs[0].legend(loc="upper left", fontsize=9)
fig.suptitle("Cada campana fina és $\\alpha_i y_i K(x_i, x)$; la frontera és on la suma creua el 0")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
La suma feta a mà i `decision_function` coincideixen fins a l'últim decimal: el model no
és res més que aquestes campanes sumades. Amb $\gamma$ petit les campanes són amples, se
solapen i la suma surt suau. Amb $\gamma$ gran cada campana és una agulla: la suma
s'arruga al voltant de cada mostra i, lluny de totes, queda plana al valor de $b$. El
model només «sap» alguna cosa just a sobre de cada mostra.
"""))

# ---------------------------------- 9. marge tou
A(md(r"""
## 9. Quan no hi ha solució possible: el marge tou

Tornem al problema del punt 3:

$$\min_{w,b} \; \frac{1}{2}\|w\|^2
\qquad \text{subjecte a} \qquad y_i(w \cdot x_i + b) \ge 1 \;\; \forall i$$

Hi ha un cas en què aquest problema **no té cap solució**: si les dues
classes se solapen, no existeix cap $(w, b)$ que compleixi les restriccions
de totes les mostres a la vegada. Un punt de la classe positiva que hagi
caigut enmig dels negatius no pot estar simultàniament a la banda positiva i
allà on és. El problema és **infactible**.

I això no és un cas rar: és el cas normal amb dades reals.

La solució és **relaxar** les restriccions, però cobrant per la relaxació.
S'afegeix una variable nova per cada mostra, $\xi_i \ge 0$ (xi, lletra
grega), que mesura **quant se salta la restricció la mostra $i$**:

$$y_i(w \cdot x_i + b) \ge 1 - \xi_i, \qquad \xi_i \ge 0$$

Si $\xi_i = 0$, la mostra compleix la restricció original. Si
$\xi_i = 0{,}3$, s'ha ficat una mica dins de la banda. Si $\xi_i > 1$, ha
creuat la frontera i està mal classificada.

Amb això sol, la solució seria trivial: posar tots els $\xi_i$ enormes i
oblidar-se de les restriccions. Per evitar-ho, els $\xi_i$ entren a
l'objectiu amb un preu:

$$\boxed{\;\min_{w,\,b,\,\xi} \; \frac{1}{2}\|w\|^2 + C\sum_i \xi_i
\qquad \text{subjecte a} \quad y_i(w \cdot x_i + b) \ge 1 - \xi_i,
\quad \xi_i \ge 0\;}$$

**Aquest $C$ és el `C` de `SVC`.** No és un paràmetre inventat pels
programadors de `scikit-learn`: és el preu de cada unitat de violació de les
restriccions.

- **$C$ gran**: violar surt car. L'optimitzador prefereix un $\|w\|$ gran
  (marge estret) abans que pagar $\xi$. Frontera dura, pocs punts dins de la
  banda.
- **$C$ petit**: violar surt barat. L'optimitzador accepta molts $\xi$ a
  canvi d'un $\|w\|$ petit (marge ample). Frontera tova, molts punts dins de
  la banda.

I ara la conseqüència que lliga amb el punt 5. La folgança complementària del
problema tou té un cas més: els multiplicadors queden **acotats**,
$0 \le \alpha_i \le C$, i un punt és vector de suport si $\alpha_i > 0$, que
ara inclou els punts de dins de la banda i els mal classificats. Per tant:
**si baixeu `C`, la banda s'engreixa, hi entren més punts i hi ha més
vectors de suport.** Comprovem-ho.
"""))

A(code(r"""
X_solapa, y_solapa = make_blobs(
    n_samples=200, centers=[[0.0, 0.0], [2.5, 2.5]],
    cluster_std=1.1, random_state=42)

plt.figure(figsize=(7, 6))
plt.scatter(X_solapa[y_solapa == 0, 0], X_solapa[y_solapa == 0, 1],
            label="classe 0", alpha=0.8)
plt.scatter(X_solapa[y_solapa == 1, 0], X_solapa[y_solapa == 1, 1],
            label="classe 1", alpha=0.8)
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.title("Dues classes que se solapen: cap recta les separa del tot")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

model_dur = SVC(kernel="linear", C=1e6).fit(X_solapa, y_solapa)
print(f"amb C molt gran (1e6) l'exactitud d'entrenament és "
      f"{model_dur.score(X_solapa, y_solapa):.1%}: ni forçant el màxim s'arriba "
      f"al 100 %")
"""))

A(code(r"""
ym = 2 * y_solapa - 1               # de {0,1} a {-1,+1}, com vol la fórmula

files = []
for C in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
    m = SVC(kernel="linear", C=C).fit(X_solapa, y_solapa)
    ww, bb = m.coef_[0], m.intercept_[0]
    # xi_i òptim per a aquesta frontera: el que falta per arribar a 1
    xi = np.maximum(0.0, 1.0 - ym * (X_solapa @ ww + bb))
    files.append({
        "C": C,
        "vectors de suport": len(m.support_),
        "||w||": np.linalg.norm(ww),
        "marge 2/||w||": 2 / np.linalg.norm(ww),
        "suma de xi": xi.sum(),
        "xi > 0": int((xi > 1e-9).sum()),
        "exactitud entren.": m.score(X_solapa, y_solapa),
    })

taula_C = pd.DataFrame(files).set_index("C").round(4)
print(taula_C.to_string())
"""))

A(md(r"""
Els números de la taula:

| `C` | vectors de suport | marge $2/\|w\|$ | $\sum \xi_i$ | mostres amb $\xi_i > 0$ |
|---|---|---|---|---|
| 0,001 | 182 | 6,4848 | 86,88 | 182 |
| 0,01 | 78 | 3,1324 | 36,12 | 77 |
| 0,1 | 36 | 1,7975 | 23,17 | 36 |
| 1 | 25 | 1,1945 | 21,14 | 24 |
| 10 | 23 | 1,0381 | 20,96 | 22 |
| 100 | 23 | 1,0383 | 20,96 | 22 |

De `C=0,001` a `C=10` els vectors de suport baixen de **182 a 23** i el marge
s'estreny de **6,4848 a 1,0381**. Amb `C=0,001` la violació és tan barata que
el model obre una banda enorme on cauen **182 de les 200 mostres**, i per això
gairebé tot el conjunt és vector de suport. El resultat del punt 5 no s'ha
trencat: segueix sent cert que només els punts amb $\alpha_i > 0$ compten. El
que ha passat és que, amb la banda tan ampla, gairebé tots els punts hi són a
dins.

Entre `C=10` i `C=100` ja no canvia res: amb aquest conjunt, un preu de 10 per
unitat de violació ja és prou dissuasiu i pujar-lo més no altera la solució.

Notareu també que l'exactitud d'entrenament es mou poc (entre 95,0 % i
96,5 %). `C` no serveix per encertar més a l'entrenament: serveix per decidir
**com de disposat estàs a acceptar errors a canvi d'un marge més ample**, i
això és una decisió sobre la generalització, no sobre l'entrenament.

Vegem-ho dibuixat.
"""))

A(code(r"""
def dibuixa_marge(ax, C):
    m = SVC(kernel="linear", C=C).fit(X_solapa, y_solapa)
    ww, bb = m.coef_[0], m.intercept_[0]

    ax.scatter(X_solapa[:, 0], X_solapa[:, 1], c=y_solapa,
               cmap="coolwarm", s=18, edgecolors="k", linewidths=0.3)
    ax.scatter(m.support_vectors_[:, 0], m.support_vectors_[:, 1],
               s=110, facecolors="none", edgecolors="tab:green", linewidths=1.2)

    x1_l = np.linspace(X_solapa[:, 0].min() - 0.5, X_solapa[:, 0].max() + 0.5, 100)
    for nivell, estil in [(0, "-"), (1, "--"), (-1, "--")]:
        ax.plot(x1_l, (nivell - bb - ww[0] * x1_l) / ww[1], estil,
                color="black", alpha=0.9 if nivell == 0 else 0.5)

    ax.set_xlim(X_solapa[:, 0].min() - 0.5, X_solapa[:, 0].max() + 0.5)
    ax.set_ylim(X_solapa[:, 1].min() - 0.5, X_solapa[:, 1].max() + 0.5)
    ax.set_xlabel("$x_1$")
    ax.set_title(f"C = {C}\n{len(m.support_)} vectors de suport, "
                 f"marge = {2 / np.linalg.norm(ww):.3f}", fontsize=10)


fig, axs = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)
dibuixa_marge(axs[0], 0.01)
dibuixa_marge(axs[1], 10.0)
axs[0].set_ylabel("$x_2$")
fig.suptitle("El preu de violar les restriccions decideix l'amplada de la banda "
             "(cercles verds: vectors de suport)")
plt.tight_layout()
plt.show()
"""))

A(md(r"""
A l'esquerra (`C=0,01`) la banda és tan ampla que engoleix mig conjunt: 78
vectors de suport. A la dreta (`C=10`) la banda és fina i només 23 punts la
toquen o la creuen. Les dues fronteres encerten gairebé el mateix a
l'entrenament; el que canvia és **de quants punts depèn el model**.
"""))

# ---------------------------------- exercicis
A(md(r"""
## 10. Pràctica

Quatre exercicis. A cadascun teniu una línia de **com saps que ho has fet
bé** amb el resultat que ha de sortir. Si no us surt això, hi ha alguna cosa
a revisar.
"""))

A(md(r"""
### Exercici 1 — Un altre problema amb restricció, per Lagrange

Resoleu

$$\min_{x,y} \; f(x,y) = x^2 + y^2
\qquad \text{subjecte a} \qquad 2x + y = 5$$

de dues maneres: (a) amb el lagrangià
$\mathcal{L} = f - \lambda(2x + y - 5)$, plantejant les tres derivades
parcials igualades a zero i resolent el sistema lineal amb
`np.linalg.solve`; (b) amb `scipy.optimize.minimize` i `constraints`.

Aneu amb compte amb el gradient de la restricció: ara $\nabla g = (2, 1)$, no
$(1,1)$ com al punt 4.

**Com saps que ho has fet bé:** la diferència entre el resultat del sistema
lineal i el de `scipy` ha de ser inferior a $10^{-5}$. El punt que trobeu ha de
complir la restricció, $2x + y = 5$, i al punt s'ha de complir la condició de
tangència: $\nabla f = (2x,\ 2y)$ ha de ser exactament $\lambda$ vegades
$\nabla g = (2, 1)$, amb la mateixa $\lambda$ a les dues components. Si
alguna d'aquestes tres coses falla, revisa les derivades parcials del lagrangià.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix, amb un problema **inventat** que no és el
vostre: $\min\ x^2 + 3y^2$ amb la restricció $x - y = 2$. Les corbes de nivell ara són
el·lipses. Aquí el punt de tangència no s'ha trobat amb Lagrange sinó **a la força
bruta**, recorrent la recta i quedant-nos amb el valor més petit de $f$: és una
manera de comprovar el que us surti amb `np.linalg.solve`.
"""))

A(code(r"""
f_il = lambda X_, Y_: X_ ** 2 + 3 * Y_ ** 2           # objectiu inventat
xs_il = np.linspace(-2, 4, 60001)
ys_il = xs_il - 2                                     # la recta x - y = 2
k_il = f_il(xs_il, ys_il).argmin()
p_il = np.array([xs_il[k_il], ys_il[k_il]])

e1, e2 = np.meshgrid(np.linspace(-1, 3.5, 300), np.linspace(-2.5, 2, 300))
fig, ax = plt.subplots(figsize=(7, 6))
cs = ax.contour(e1, e2, f_il(e1, e2), levels=[0.5, 1.5, f_il(*p_il), 5, 8], colors="tab:gray")
ax.clabel(cs, inline=True, fontsize=8, fmt="f=%.1f")
ax.plot(xs_il, ys_il, color="tab:red", linewidth=2, label="restricció inventada $x - y = 2$")
ax.scatter(*p_il, color="black", s=80, zorder=5, label=f"força bruta: ({p_il[0]:.2f}, {p_il[1]:.2f})")
gf_il = np.array([2 * p_il[0], 6 * p_il[1]])
ax.annotate("", xy=p_il + 0.25 * gf_il, xytext=p_il,
            arrowprops=dict(arrowstyle="->", color="tab:green", lw=2))
ax.annotate("", xy=p_il + 0.4 * np.array([1, -1]), xytext=p_il,
            arrowprops=dict(arrowstyle="->", color="tab:purple", lw=2, linestyle=":"))
ax.plot([], [], color="tab:green", label=r"$\nabla f$")
ax.plot([], [], color="tab:purple", linestyle=":", label=r"$\nabla g$")
ax.set_xlim(-1, 3.5)
ax.set_ylim(-2.5, 2)
ax.set_aspect("equal")
ax.set_title("Problema inventat: on la recta toca una el·lipse")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
plt.show()
"""))

A(code(r"""
# (a) Plantejament amb el lagrangià L = x^2 + y^2 - lambda*(2x + y - 5).
#     Escriu les tres equacions dL/dx = 0, dL/dy = 0, dL/dlambda = 0 com un
#     sistema lineal de 3x3 en (x, y, lambda) i resol-lo amb np.linalg.solve.

# (b) El mateix amb scipy.optimize.minimize, passant la restricció com un
#     diccionari {"type": "eq", "fun": ...}.

# (c) Imprimeix les dues solucions i la diferència màxima entre elles.
"""))

A(md(r"""
### Exercici 2 — Folgança complementària en un altre conjunt

Repetiu la comprovació del punt 5 amb una parella d'espècies diferent:
**setosa contra virginica**, amb les columnes `petal_llarg` i `petal_ample`.
Entreneu un `SVC(kernel="linear", C=1e5)` i comproveu:

1. Que tots els vectors de suport compleixen $|w \cdot x_i + b| \approx 1$.
2. Que cap de les altres mostres baixa d'1.
3. Que $w$ reconstruït amb `dual_coef_ @ support_vectors_` coincideix amb
   `coef_`.

Imprimiu els números, no només un `True`.

**Com saps que ho has fet bé:** les tres comprovacions de l'enunciat són la
prova, i han de sortir com al punt 5: $|w \cdot x_i + b|$ dels vectors de suport
igual a 1 fins a un error petit (amb `C=1e5`, de l'ordre de $10^{-7}$ o menys),
cap altra mostra per sota d'1, i el $w$ reconstruït igual a `coef_` (diferència 0
o de l'ordre de l'arrodoniment). A més, `n_support_` ha de tenir almenys un vector
de suport de **cada** espècie: sense un a cada costat no hi hauria marge. Quants
n'hi ha i com de lluny queda la resta, ho llegeixes tu.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix: com es llegeix la comprovació. Dades
**inventades** (dos núvols separats) i un `SVC(kernel="linear", C=1e5)`. L'histograma
és $|w \cdot x_i + b|$ de les mostres que **no** són vectors de suport; les línies
vermelles, els vectors de suport. Si la folgança complementària es compleix, les
vermelles cauen totes a 1 i l'histograma comença a la dreta d'1.
"""))

A(code(r"""
X_il, y_il = make_blobs(n_samples=80, centers=[[0, 0], [4, 3]], cluster_std=0.7, random_state=5)
m_il = SVC(kernel="linear", C=1e5).fit(X_il, y_il)
val_il = np.abs(m_il.decision_function(X_il))
sup_il = np.zeros(len(X_il), dtype=bool)
sup_il[m_il.support_] = True

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(val_il[~sup_il], bins=25, color="tab:blue", alpha=0.7,
        label=f"{(~sup_il).sum()} mostres que no són de suport")
for v in val_il[sup_il]:
    ax.axvline(v, color="tab:red", linewidth=2)
ax.plot([], [], color="tab:red", linewidth=2, label=f"{sup_il.sum()} vectors de suport")
ax.axvspan(0, 1, color="tab:gray", alpha=0.15)
ax.annotate("aquí no hi pot\nhaver ningú", (0.1, ax.get_ylim()[1] * 0.75))
ax.set_xlim(0, val_il.max() * 1.05)
ax.set_xlabel("$|w \cdot x_i + b|$")
ax.set_ylabel("quantes mostres")
ax.set_title("Dades inventades: els vectors de suport a 1, la resta per sobre")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
plt.show()
"""))

A(code(r"""
# Construeix el subconjunt setosa + virginica a partir del DataFrame `dades`
# (la columna d'espècie es diu "especie") i codifica y com 0/1.

# Entrena SVC(kernel="linear", C=1e5), calcula w, b i el vector de valors
# w . x_i + b per a totes les mostres.

# Separa vectors de suport (model.support_) de la resta i imprimeix:
#   - |w.x+b| de cada vector de suport
#   - mínim, mitjana i màxim de |w.x+b| de la resta, i quantes baixen d'1

# Reconstrueix w amb dual_coef_ @ support_vectors_ i imprimeix la diferència
# amb coef_.
"""))

A(md(r"""
### Exercici 3 — Kernel i transformació per a $(a \cdot b + 1)^2$

Al punt 7 vau veure que $(a \cdot b)^2$ correspon a
$\phi(x) = (x_1^2,\ \sqrt{2}x_1x_2,\ x_2^2)$. Ara toca el kernel

$$K(a, b) = (a \cdot b + 1)^2$$

Desenvolupeu-lo a mà en un paper. El resultat és

$$K(a,b) = 1 + 2a_1b_1 + 2a_2b_2 + a_1^2b_1^2 + 2a_1a_2b_1b_2 + a_2^2b_2^2$$

i d'aquí es llegeix la transformació, que té **sis** coordenades:

$$\phi(x) = \left(1,\; \sqrt{2}x_1,\; \sqrt{2}x_2,\;
x_1^2,\; \sqrt{2}x_1x_2,\; x_2^2\right)$$

Implementeu les dues bandes amb NumPy i comproveu que coincideixen per a 5
parelles de punts a l'atzar generats amb `rng = np.random.default_rng(7)`.

Fixeu-vos en la diferència respecte del punt 7: aquest kernel té els termes
de grau 1 i el terme constant, no només els de grau 2. El `+1` de dins del
parèntesi és exactament el que els fa aparèixer. Això és el que fa `SVC` amb
`kernel="poly"` i `coef0=1`.

**Com saps que ho has fet bé:** la diferència màxima entre les dues bandes ha
de ser de l'ordre de $10^{-15}$ o menys. Amb `default_rng(7)`, el primer
valor de $K$ ha de ser aproximadament **1,2259**. Si us surt una diferència
gran, el més probable és que hàgiu posat un $\sqrt{2}$ on no toca o us
n'hàgiu deixat un.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix: com es veu que les dues bandes coincideixen.
Aquí ho fem amb el kernel del punt 7, $(a \cdot b)^2$, no amb el vostre. Cada punt és una
parella: a l'eix horitzontal $K(a, b)$ calculat directament, al vertical
$\phi(a) \cdot \phi(b)$. Si la $\phi$ és bona, tots cauen sobre la diagonal (esquerra).
A la dreta, la mateixa $\phi$ **sense** els $\sqrt{2}$: els punts se n'escapen. És
l'error que diu l'enunciat, i es veu d'una ullada.
"""))

A(code(r"""
rng_il = np.random.default_rng(99)
a_il, b_il = rng_il.normal(size=(40, 2)), rng_il.normal(size=(40, 2))
phi_mal_il = lambda Z: np.column_stack([Z[:, 0] ** 2, Z[:, 0] * Z[:, 1], Z[:, 1] ** 2])  # sense sqrt(2)

k_il = kernel_poly2(a_il, b_il)
fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
for ax, phi_f, titol in [(axs[0], phi_poly2, "phi correcta"), (axs[1], phi_mal_il, "phi sense els $\sqrt{2}$")]:
    ax.scatter(k_il, np.sum(phi_f(a_il) * phi_f(b_il), axis=1), color="tab:blue", edgecolor="k")
    lim = [0, k_il.max() * 1.05]
    ax.plot(lim, lim, color="tab:red", linestyle="--", label="diagonal: les dues bandes iguals")
    ax.set_xlabel("$K(a, b)$ directe")
    ax.set_title(titol)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("$\phi(a) \cdot \phi(b)$")
fig.suptitle("Kernel del punt 7 amb parelles inventades: sobre la diagonal o no")
plt.tight_layout()
plt.show()
"""))

A(code(r"""
# Defineix phi_poly2_mes1(Z) que retorni les 6 coordenades per cada fila de Z.

# Defineix el kernel directe: (suma(a*b, eix 1) + 1) ** 2.

# rng = np.random.default_rng(7); genera punts_a i punts_b de forma (5, 2).

# Compara les dues bandes parella a parella i imprimeix la diferència màxima.
"""))

A(md(r"""
### Exercici 4 — Com creix el nombre de vectors de suport en baixar `C`

Al punt 9 ho vau veure amb dades artificials. Repetiu-ho amb dades reals:
**versicolor contra virginica**, amb `petal_llarg` i `petal_ample`. Aquestes
dues espècies se solapen de veritat.

Per a `C` a `[0.01, 0.1, 1, 10, 100]`, entreneu un `SVC(kernel="linear")` i
munteu una taula amb el nombre de vectors de suport, $\|w\|$, el marge
$2/\|w\|$ i l'exactitud d'entrenament. Feu un gràfic del nombre de vectors de
suport en funció de `C`, amb l'eix de `C` en escala logarítmica
(`plt.xscale("log")`).

**Com saps que ho has fet bé:** a cada fila, el marge ha de ser exactament 2
dividit per la columna de $\|w\|$, i $\|w\|$ ha de coincidir amb
`np.linalg.norm(model.coef_)`. El nombre de vectors de suport ha de ser
`model.n_support_.sum()`, i no pot passar del nombre de flors que entreneu (100)
ni baixar de 2, un per espècie com a mínim. Cap a on es mou cada columna quan puja
`C`, i què li passa a l'exactitud, ho llegeixes tu a la taula i al gràfic.
"""))

A(md(r"""
Abans de començar, la idea en un dibuix: com es llegeix un eix de `C` en escala
logarítmica. Dades **inventades** (dos núvols que se solapen, diferents dels del punt
9). Amb escala log, els valors 0,01, 0,1, 1, 10 i 100 queden a la mateixa distància
l'un de l'altre: cada pas és multiplicar per 10. Sense l'escala log, tots els punts de
l'esquerra s'amuntegarien a sobre del zero.
"""))

A(code(r"""
X_il, y_il = make_blobs(n_samples=150, centers=[[0, 0], [2, 2]], cluster_std=1.0, random_state=9)
Cs_il = [0.01, 0.1, 1, 10, 100]
n_sv_il = [len(SVC(kernel="linear", C=c).fit(X_il, y_il).support_) for c in Cs_il]

fig, axs = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
for ax, escala in zip(axs, ["linear", "log"]):
    ax.plot(Cs_il, n_sv_il, "o-", color="tab:blue")
    ax.set_xscale(escala)
    ax.set_xlabel(f"C (escala {'lineal' if escala == 'linear' else 'logarítmica'})")
    ax.set_title(f'plt.xscale("{escala}")')
    ax.grid(alpha=0.3)
axs[0].set_ylabel("vectors de suport")
fig.suptitle("Dades inventades: el mateix gràfic amb les dues escales")
plt.tight_layout()
plt.show()
"""))

A(code(r"""
# Construeix el subconjunt versicolor + virginica amb petal_llarg i petal_ample.

# Per a cada C de [0.01, 0.1, 1, 10, 100]: entrena, i guarda en una llista de
# diccionaris el nombre de vectors de suport, ||w||, 2/||w|| i l'exactitud.

# Mostra la taula amb pd.DataFrame i dibuixa vectors de suport en funció de C
# amb plt.xscale("log"). Etiqueta els dos eixos en català.
"""))

# ---------------------------------- resum
A(md(r"""
## 11. Resum

Què s'ha **demostrat** en aquest quadern, no què s'ha explicat:

- Que $w$ és perpendicular a la frontera $w \cdot x + b = 0$, restant les
  equacions de dos punts qualssevol de la frontera. Comprovat: producte
  escalar `0.0`.
- Que la distància d'un punt a la frontera és $|w \cdot x_0 + b| / \|w\|$,
  deduïda projectant sobre el vector normal unitari. Comprovada contra una
  cerca per força bruta sobre 400.001 punts de la recta.
- Que fixar $|w \cdot x_i + b| = 1$ als punts més propers **no perd
  generalitat**: escalar $(w, b)$ per una constant no mou la frontera ni les
  prediccions, només reescala els números. Comprovat: prediccions idèntiques
  i distàncies iguals fins a $8{,}88 \cdot 10^{-16}$ després de multiplicar
  per 5. I sota aquesta normalització, $2/\|w\| = 1{,}272792$ és exactament el
  doble del marge geomètric $0{,}636396$.
- Que maximitzar el marge $2/\|w\|$ **és** minimitzar $\frac{1}{2}\|w\|^2$
  subjecte a $y_i(w \cdot x_i + b) \ge 1$.
- Que un problema amb restricció d'igualtat es resol pel lagrangià, i que la
  seva solució és on $\nabla f = \lambda \nabla g$, és a dir on la restricció
  és tangent a una corba de nivell de l'objectiu. Comprovat per tres camins
  independents, tots tres a $(0{,}5,\ 0{,}5)$.
- Que la condició de folgança complementària
  $\alpha_i[y_i(w \cdot x_i + b) - 1] = 0$ **obliga** cada punt a estar en un
  de dos estats: no influir gens ($\alpha_i = 0$) o estar exactament sobre el
  marge. **Els vectors de suport són una conseqüència matemàtica d'aquesta
  condició, no una optimització d'enginyeria.** Comprovat sobre Iris: 2
  vectors de suport amb $|w \cdot x_i + b|$ = 0,99999987 i 0,99999980, i 98
  mostres amb un mínim d'1,16470573. Repetit amb els sèpals: 4 vectors de
  suport a 1,00031 i 96 mostres amb un mínim d'1,10561120.
- Que $w = \sum_i \alpha_i y_i x_i$, una combinació lineal **només** dels
  vectors de suport. Comprovat: diferència **0,0** contra el `coef_` de
  `scikit-learn` amb el producte de matrius, i $2{,}13 \cdot 10^{-14}$ amb el
  bucle explícit, que és la mateixa suma en un altre ordre.
- Que el truc del kernel és una identitat algebraica i no una operació
  misteriosa: $(a \cdot b)^2 = \phi(a) \cdot \phi(b)$ amb
  $\phi(x) = (x_1^2, \sqrt{2}x_1x_2, x_2^2)$. Comprovat amb una diferència
  màxima de $2{,}64 \cdot 10^{-16}$ parella a parella i
  $1{,}78 \cdot 10^{-15}$ per a la matriu sencera.
- Que el kernel RBF correspon a una transformació de **dimensió infinita**
  (sèrie de Taylor de l'exponencial: una suma infinita de kernels polinòmics)
  i que això no impedeix res, perquè el dual només demana productes escalars.
  La nostra implementació coincideix amb la de `scikit-learn` fins a
  $1{,}11 \cdot 10^{-16}$.
- Que el `C` de `SVC` és el **preu de violar una restricció** al problema de
  marge tou $\frac{1}{2}\|w\|^2 + C\sum_i\xi_i$. Comprovat: de `C=0,001` a
  `C=10`, els vectors de suport baixen de 182 a 23 i el marge s'estreny de
  6,4848 a 1,0381, mentre l'exactitud d'entrenament es mou només entre
  95,0 % i 96,5 %.

### El que no s'ha demostrat, i cal saber-ho

- **No hem derivat el problema dual.** L'hem escrit i hem verificat les seves
  conseqüències amb models entrenats. La substitució de
  $w = \sum \alpha_i y_i x_i$ dins del lagrangià i l'eliminació de $b$ és un
  càlcul que no hem fet.
- **No hem demostrat que les condicions KKT siguin necessàries a l'òptim.**
  Les hem agafades com a resultat donat. La demostració demana teoria de
  convexitat i dualitat.
- **No hem construït la $\phi$ del kernel RBF**, perquè té infinites
  coordenades. Només hem ensenyat per què és infinita.
- **No hem resolt cap SVM nosaltres.** Hem plantejat el problema i hem
  verificat la solució que dóna `libsvm` a través de `SVC`. Els mètodes que
  el resolen (SMO i companyia) són un tema a part.
"""))

info = escriu(cells, DESTI, titol_colab="MA_05_marge_optimitzacio.ipynb")
print(info)
