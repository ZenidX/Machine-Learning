# -*- coding: utf-8 -*-
"""Genera el quadern MA_01_algebra_lineal.ipynb.

Els numeros que apareixen al text son els reals que surten en executar el
quadern amb numpy 2.3 i scikit-learn 1.8 (comprovar-ho amb _eines/executa_nb.py).
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

DESTI = "Machine Learning/03_matematiques/MA_01_algebra_lineal.ipynb"

cells = []

# ---------------------------------------------------------------- portada
cells.append(md(r"""
# L'àlgebra lineal que ja feu servir

**Optativa d'Aprenentatge automàtic — DAM/DAW 2n**

Als quaderns dels cinc models vau calcular distàncies, vau dibuixar fronteres i vau
mirar coeficients. Tot allò era àlgebra lineal, però no se li va posar el nom.

Aquest quadern li posa el nom. No introdueix cap model nou: agafa el que ja heu fet i
ensenya què hi havia a sota. L'objectiu és que al final pugueu dir aquesta frase i
saber per què és certa: **un model entrenat és un vector de números, i predir és
multiplicar.**

No cal que hàgiu fet àlgebra lineal abans. Tot el que necessitem es defineix aquí. El
que sí que donem per sabut és numpy: arrays, indexació i agregacions per eixos.

El pla:

1. Un vector és un punt i una fletxa.
2. La norma: la mida d'un vector.
3. La distància euclidiana és la norma d'una diferència (aquí es tanca el cercle amb k-NN).
4. El producte escalar, i l'angle que en surt.
5. La projecció d'un vector sobre un altre.
6. Una matriu és una taula i també una transformació.
7. La frontera de la regressió logística és un producte de matrius.
8. La transposada, i per què apareix pertot.

Cada fórmula va seguida de la línia de numpy que la calcula, i al final de cada apartat
es comprova que el número fet a mà i el de la llibreria coincideixen.
"""))

cells.append(code(r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data                 # 150 files (flors) x 4 columnes (mesures)
y = iris.target               # 0 = setosa, 1 = versicolor, 2 = virginica
noms_mesures = ["sepal_llarg", "sepal_ample", "petal_llarg", "petal_ample"]

print("Forma de X:", X.shape)
print("Mesures:", noms_mesures)
print("Espècies:", ", ".join(iris.target_names))
"""))

# ---------------------------------------------------------------- 1. vector
cells.append(md(r"""
## 1. Un vector no és una llista de números

Al codi, `X[0]` és un array de 4 números. En àlgebra lineal aquest objecte té un nom i
dues lectures.

**Primera lectura: un punt.** La flor número 0 té quatre mesures, i aquestes quatre
mesures són les seves coordenades. Igual que $(3, 5)$ és un punt en un pla i $(3, 5, 2)$
és un punt en l'espai, $(5.1,\ 3.5,\ 1.4,\ 0.2)$ és **un punt en un espai de 4
dimensions**. No el podeu dibuixar. Això no impedeix calcular-hi res.

**Segona lectura: una fletxa.** El mateix vector és la fletxa que va de l'origen fins a
aquest punt. Aquesta lectura sembla innecessària ara i serà la important a partir de
l'apartat 4: les fletxes tenen llargada i tenen direcció, i les dues coses es poden
mesurar.

Escrivim el vector en notació matemàtica. Un vector de $n$ components:

$$v = (v_1, v_2, \dots, v_n)$$

Compte amb un detall d'índexs: en matemàtiques es compta des de 1 i a numpy des de 0. El
$v_1$ de la fórmula és el `v[0]` del codi.
"""))

cells.append(code(r"""
v = X[0]                      # la primera flor del dataset

print("El vector v:", v)
print("Quantes components té (n):", v.shape[0])
print("v_1 de la fórmula = v[0] del codi =", v[0])
print("Espècie d'aquesta flor:", iris.target_names[y[0]])
"""))

cells.append(md(r"""
De les 4 dimensions en podem dibuixar dues. Agafem les del pètal, que són les que separen
millor les espècies, i mirem les 150 flors com el que són: 150 punts.

La flor 0 la marquem amb la fletxa des de l'origen, per veure les dues lectures alhora:
el punt on cau, i la fletxa que hi arriba.
"""))

cells.append(code(r"""
plt.figure(figsize=(7, 5.5))

for classe, nom in enumerate(iris.target_names):
    mascara = y == classe
    plt.scatter(X[mascara, 2], X[mascara, 3], s=35, alpha=0.7, label=nom)

# la flor 0, dibuixada com a fletxa des de l'origen
plt.annotate("", xy=(X[0, 2], X[0, 3]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="black", linewidth=1.8))
plt.scatter([X[0, 2]], [X[0, 3]], color="black", s=70, zorder=3,
            label="flor 0 (com a fletxa)")

plt.xlim(0, 7.5)
plt.ylim(0, 3)
plt.xlabel("Llargada del pètal (cm)")
plt.ylabel("Amplada del pètal (cm)")
plt.title("Cada flor és un punt; el vector és la fletxa que hi arriba")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

cells.append(md(r"""
El dibuix té dues dimensions perquè només en podem dibuixar dues. Les flors de veritat
viuen en 4. Les tres taques que es veuen separades hi continuen sent separades; el que
perdem en dibuixar-ne dues és informació, no els punts.

A partir d'aquí tot el que farem val per a $n$ qualsevol. Ho comprovarem amb $n = 2$
perquè ho podem dibuixar, i l'aplicarem amb $n = 4$ perquè són les dades reals.
"""))

# ---------------------------------------------------------------- 2. norma
cells.append(md(r"""
## 2. La norma: la mida d'un vector

La **norma** d'un vector és la llargada de la seva fletxa. S'escriu amb dues barres i es
defineix així:

$$\|v\| = \sqrt{\sum_{i=1}^{n} v_i^2}$$

Llegida en veu alta: eleva al quadrat cada component, suma-ho tot, i fes l'arrel.

**Això és el teorema de Pitàgoras.** Amb $n = 2$, la fórmula diu
$\|v\| = \sqrt{v_1^2 + v_2^2}$, que és la hipotenusa d'un triangle rectangle de catets
$v_1$ i $v_2$. Amb $n = 4$ és la mateixa operació amb dos sumands més. La norma és
Pitàgoras estès a $n$ dimensions, i no hi ha res més a l'ampliació: cap idea nova, dos
sumands més.

Primer la implementem, després la comparem amb `np.linalg.norm`.
"""))

cells.append(code(r"""
v = X[0]

# la fórmula, pas per pas
quadrats = v ** 2                      # v_i^2
suma = np.sum(quadrats)                # sum_i v_i^2
norma_a_ma = np.sqrt(suma)             # l'arrel

norma_numpy = np.linalg.norm(v)        # el que fa la llibreria

print("v        =", v)
print("quadrats =", quadrats)
print("suma     =", suma)
print(f"norma a mà     = {norma_a_ma:.6f}")
print(f"np.linalg.norm = {norma_numpy:.6f}")
print("Coincideixen:", np.isclose(norma_a_ma, norma_numpy))
"""))

cells.append(md(r"""
`6.345077` en els dos casos. La norma d'aquesta flor és 6.35, i les unitats són
centímetres barrejats de quatre mesures diferents: és un número sense significat biològic.
La norma d'un vector de dades brut rarament vol dir res. El que vol dir molt és la norma
d'una **diferència**, i això és l'apartat següent.

Abans, la comprovació que hem promès: amb $n = 2$ ha de donar Pitàgoras.
"""))

cells.append(code(r"""
u = np.array([3.0, 4.0])               # el triangle 3-4-5 de tota la vida

print("Norma amb la fórmula general:", np.linalg.norm(u))
print("Pitàgoras a mà:", np.sqrt(3.0 ** 2 + 4.0 ** 2))
print("Coincideixen:", np.isclose(np.linalg.norm(u), 5.0))
"""))

# ---------------------------------------------------------------- 3. distancia
cells.append(md(r"""
## 3. La distància euclidiana és la norma d'una diferència

La distància entre dos punts $a$ i $b$ és la llargada de la fletxa que va de l'un a
l'altre. Aquella fletxa és el vector $a - b$. Per tant:

$$d(a, b) = \|a - b\| = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}$$

**Aquí es tanca un cercle.** Aquesta fórmula de la dreta és exactament la que vau
implementar al quadern de k-NN, quan calculàveu com s'assemblen dues flors. Llavors se'n
deia distància euclidiana i es justificava amb Pitàgoras. Ara té un altre nom: és **la
norma d'una diferència**. La fórmula no ha canviat ni un signe; el que ha canviat és que
ara sabem que la distància i la mida són la mateixa operació aplicada a coses diferents.

Al quadern de k-NN les dues flors de l'exemple eren `X[0]` (setosa) i `X[50]`
(versicolor), i la distància amb les 4 mesures sortia `4.00`. Reproduïm el número.
"""))

cells.append(code(r"""
a = X[0]      # setosa
b = X[50]     # versicolor

diferencia = a - b

dist_a_ma = np.sqrt(np.sum(diferencia ** 2))     # la fórmula del quadern de k-NN
dist_com_norma = np.linalg.norm(a - b)           # la mateixa cosa, dita amb la norma

print("a =", a)
print("b =", b)
print("a - b =", diferencia)
print(f"sqrt(sum((a-b)^2))  = {dist_a_ma:.6f}")
print(f"np.linalg.norm(a-b) = {dist_com_norma:.6f}")
print("Coincideixen:", np.isclose(dist_a_ma, dist_com_norma))
print(f"Arrodonit com al quadern de k-NN: {dist_a_ma:.2f}")
"""))

cells.append(md(r"""
`4.003748`, que arrodonit és el `4.00` del quadern de k-NN. Mateix número, mateixes flors,
dues maneres d'escriure-ho.

Val la pena dir que això és el que fa `KNeighborsClassifier` quan el crideu, repetit per a
cada parella de flors que li interessa: restes, quadrats, sumes i arrels. Res més.
"""))

# ---------------------------------------------------------------- 4. producte escalar
cells.append(md(r"""
## 4. El producte escalar

El **producte escalar** de dos vectors és un sol número. Té dues definicions que semblen
no tenir res a veure, i són la mateixa.

**Definició algebraica** (la que es programa):

$$a \cdot b = \sum_{i=1}^{n} a_i b_i$$

Multiplica component a component i suma-ho tot.

**Definició geomètrica** (la que explica què vol dir):

$$a \cdot b = \|a\| \, \|b\| \cos\theta$$

on $\theta$ és l'angle entre les dues fletxes. Les dues normes són números positius, i
per tant **el signe del producte escalar és el signe del cosinus**: positiu si les dues
fletxes apunten cap a la mateixa banda, zero si són perpendiculars, negatiu si apunten en
sentits oposats. Aquesta frase és la que farà falta a l'apartat 7.

Comencem per la definició algebraica, amb les tres maneres d'escriure-la a numpy.
"""))

cells.append(code(r"""
a = X[0]
b = X[50]

# definició algebraica, a mà
productes = a * b                 # a_i * b_i, component a component
escalar_a_ma = np.sum(productes)  # la suma

print("a         =", a)
print("b         =", b)
print("a_i * b_i =", productes)
print("Suma (producte escalar) =", escalar_a_ma)
print("np.dot(a, b) =", np.dot(a, b))
print("a @ b        =", a @ b)
print("Coincideixen els tres:",
      np.isclose(escalar_a_ma, np.dot(a, b)) and np.isclose(escalar_a_ma, a @ b))
"""))

cells.append(md(r"""
`53.76` per les tres vies. L'operador `@` és el que fa servir tothom, i a partir d'ara el
farem servir nosaltres.

Ara la definició geomètrica. Hi ha un problema pràctic: per calcular
$\|a\| \|b\| \cos\theta$ ens cal l'angle $\theta$, i en 4 dimensions no tenim cap manera
de mesurar un angle que no passi pel producte escalar. Si l'angle el traiem del producte
escalar, comprovar que les dues definicions coincideixen no demostra res: seria un
raonament circular.

Per això la comprovació la fem en **2 dimensions**, on l'angle d'una fletxa es pot mesurar
a part amb `np.arctan2`, que dona l'angle que forma la fletxa amb l'eix horitzontal a
partir de les seves dues components. Agafem les dues mesures del pètal de les mateixes
dues flors:

- $a_2 = (1.4,\ 0.2)$, angle amb l'horitzontal: 8.130 graus
- $b_2 = (4.7,\ 1.4)$, angle amb l'horitzontal: 16.587 graus
- angle entre elles, $\theta$: 8.457 graus

Amb aquest $\theta$ mesurat per fora, calculem les dues definicions i les comparem.
"""))

cells.append(code(r"""
a2 = X[0, 2:]      # (petal_llarg, petal_ample) de la flor 0
b2 = X[50, 2:]     # les mateixes dues mesures de la flor 50

# angle de cada fletxa amb l'eix horitzontal, mesurat sense cap producte escalar
angle_a = np.arctan2(a2[1], a2[0])
angle_b = np.arctan2(b2[1], b2[0])
theta = angle_b - angle_a

esquerra = np.sum(a2 * b2)                                       # sum a_i b_i
dreta = np.linalg.norm(a2) * np.linalg.norm(b2) * np.cos(theta)  # |a||b| cos(theta)

print(f"angle de a2: {np.degrees(angle_a):.3f} graus")
print(f"angle de b2: {np.degrees(angle_b):.3f} graus")
print(f"theta entre les dues: {np.degrees(theta):.3f} graus")
print(f"definició algebraica  sum(a_i b_i)      = {esquerra:.10f}")
print(f"definició geomètrica  |a||b| cos(theta) = {dreta:.10f}")
print(f"diferència = {abs(esquerra - dreta):.2e}")
print("Coincideixen:", np.isclose(esquerra, dreta))
"""))

cells.append(md(r"""
`6.8600000000` per les dues definicions, i la diferència és `0.00e+00`. Amb altres números
la diferència sortiria de l'ordre de $10^{-16}$, que és el soroll de la coma flotant i no
un error: per això es compara amb `np.isclose` i no amb `==`.

Un cop acceptada la igualtat, la podem girar per **obtenir l'angle** a partir del producte
escalar, i això sí que val en 4 dimensions:

$$\cos\theta = \frac{a \cdot b}{\|a\| \, \|b\|} \qquad\Longrightarrow\qquad
\theta = \arccos\left(\frac{a \cdot b}{\|a\| \, \|b\|}\right)$$

Aquest quocient es diu **similitud del cosinus** i el trobareu pertot on es comparin
textos o vectors d'incrustació.
"""))

cells.append(code(r"""
cos_theta = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
theta_4d = np.arccos(cos_theta)

print(f"cos(theta) en 4 dimensions = {cos_theta:.6f}")
print(f"theta = {theta_4d:.6f} radians = {np.degrees(theta_4d):.3f} graus")
"""))

cells.append(md(r"""
`21.816` graus entre les dues flors. És un angle petit: les dues fletxes apunten cap a una
zona semblant de l'espai, tot i que els punts estiguin a distància 4.00. Angle i distància
són coses diferents i mesuren coses diferents.

El cas que importa és quan el cosinus val 0, és a dir **angle de 90 graus**. Dos vectors
perpendiculars tenen producte escalar zero. Ho comprovem amb dos vectors petits triats a
mà, i els dibuixem.
"""))

cells.append(code(r"""
p = np.array([2.0, 1.0])
q = np.array([-1.0, 2.0])

print("p @ q =", p @ q)
cos_pq = (p @ q) / (np.linalg.norm(p) * np.linalg.norm(q))
print(f"cos(theta) = {cos_pq:.1f}  ->  theta = {np.degrees(np.arccos(cos_pq)):.1f} graus")

plt.figure(figsize=(5.5, 5.5))
plt.annotate("", xy=(p[0], p[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=2))
plt.annotate("", xy=(q[0], q[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="tab:orange", linewidth=2))
plt.text(p[0] + 0.1, p[1], "p = (2, 1)", color="tab:blue")
plt.text(q[0] - 0.9, q[1] + 0.1, "q = (-1, 2)", color="tab:orange")

plt.axhline(0, color="gray", linewidth=0.8)
plt.axvline(0, color="gray", linewidth=0.8)
plt.xlim(-2.5, 2.5)
plt.ylim(-0.5, 2.5)
plt.gca().set_aspect("equal")
plt.xlabel("Primera component")
plt.ylabel("Segona component")
plt.title("Producte escalar 0: les fletxes formen 90 graus")
plt.grid(alpha=0.3)
plt.show()
"""))

# ---------------------------------------------------------------- 5. projeccio
cells.append(md(r"""
## 5. La projecció d'un vector sobre un altre

Projectar $a$ sobre $b$ és respondre aquesta pregunta: **quant de $a$ va en la direcció de
$b$?** Geomètricament és l'ombra de la fletxa $a$ sobre la recta que marca $b$, quan la
llum ve perpendicular a $b$.

L'ombra es pot donar de dues maneres. La primera és la seva llargada, un sol número, que
es diu **projecció escalar**:

$$\text{proj}_{\text{esc}}(a \to b) = \frac{a \cdot b}{\|b\|}$$

La segona és l'ombra com a vector, que apunta en la direcció de $b$ i té aquella llargada.
És la **projecció vectorial**:

$$\text{proj}(a \to b) = \frac{a \cdot b}{b \cdot b} \, b$$

D'on surt la fórmula, en dues línies: de la definició geomètrica. L'ombra de $a$ té
llargada $\|a\| \cos\theta$, que és el catet contigu del triangle rectangle del dibuix; i
com que $a \cdot b = \|a\| \|b\| \cos\theta$, dividint per $\|b\|$ queda exactament
$\|a\| \cos\theta$. La segona fórmula és la primera multiplicada per $b / \|b\|$, el
vector $b$ reduït a llargada 1, per donar-li direcció.

**Per què ens importa.** Perquè la projecció és la mesura de quant hi ha d'una direcció
dins d'un vector, i tot el que ve després són projeccions:

- la **frontera de decisió** de la logística i de l'SVM: hi ha una direcció $w$, i la
  puntuació de cada punt és la seva projecció sobre aquella direcció;
- el **marge** de l'SVM: una distància mesurada en la direcció perpendicular a la
  frontera, és a dir una projecció;
- el **PCA**: buscar les direccions on les dades tenen més variació, i projectar-hi.

Dibuixem la projecció amb les dues mesures del pètal de les flors 0 i 50.
"""))

cells.append(code(r"""
a2 = X[0, 2:]
b2 = X[50, 2:]

proj_escalar = (a2 @ b2) / np.linalg.norm(b2)
proj_vector = ((a2 @ b2) / (b2 @ b2)) * b2

print("a2 =", a2, " b2 =", b2)
print(f"projecció escalar de a2 sobre b2 = {proj_escalar:.6f}")
print("projecció vectorial =", np.round(proj_vector, 6))
print(f"norma de la projecció vectorial = {np.linalg.norm(proj_vector):.6f}")
print("La norma del vector projecció és la projecció escalar:",
      np.isclose(np.linalg.norm(proj_vector), proj_escalar))

plt.figure(figsize=(7, 4.5))
plt.annotate("", xy=(b2[0], b2[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="tab:orange", linewidth=2))
plt.annotate("", xy=(a2[0], a2[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="tab:blue", linewidth=2))
plt.annotate("", xy=(proj_vector[0], proj_vector[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="tab:green", linewidth=2.5))
# la llum perpendicular: de la punta de a2 fins a la seva ombra
plt.plot([a2[0], proj_vector[0]], [a2[1], proj_vector[1]], "k--", linewidth=1)

plt.text(b2[0] - 0.45, b2[1] + 0.1, "b2", color="tab:orange")
plt.text(a2[0] - 0.15, a2[1] + 0.12, "a2", color="tab:blue")
plt.text(proj_vector[0] - 0.35, proj_vector[1] - 0.25, "ombra de a2 sobre b2",
         color="tab:green")

plt.xlim(0, 5.5)
plt.ylim(0, 1.8)
plt.gca().set_aspect("equal")
plt.xlabel("Llargada del pètal (cm)")
plt.ylabel("Amplada del pètal (cm)")
plt.title("Projecció: l'ombra d'una fletxa sobre la direcció de l'altra")
plt.grid(alpha=0.3)
plt.show()
"""))

cells.append(md(r"""
La projecció escalar surt `1.398835`: és la llargada de la fletxa verda. La línia
discontínua és perpendicular a `b2`, i és el que fa que això sigui una ombra i no una
altra cosa.

En 4 dimensions no es pot dibuixar però es calcula igual: la projecció escalar de la flor
0 sobre la flor 50 és `(a @ b) / np.linalg.norm(b)`, que val `5.890645`.
"""))

# ---------------------------------------------------------------- 6. matrius
cells.append(md(r"""
## 6. Una matriu és una taula, i també una transformació

`X` és una matriu de 150 x 4: **150 files, una per flor; 4 columnes, una per mesura.**
Aquesta és la lectura de taula, i és la que ja teniu.

La segona lectura és la que fa falta: una matriu és una **màquina que menja vectors**. Li
doneu un vector de 4 números i en surt un vector de 150. Això és el **producte
matriu-vector**:

$$(Xw)_i = \sum_{j=1}^{4} X_{ij} \, w_j$$

Llegida amb calma: la component $i$ del resultat és el producte escalar de la **fila $i$**
de $X$ amb el vector $w$. Hi ha 150 files, per tant 150 productes escalars, per tant 150
números.

En termes de dades: **$Xw$ és una puntuació per cada flor.** El vector $w$ diu quant pesa
cada mesura, i cada flor rep un número que resumeix les seves 4 mesures segons aquells
pesos. Si $w = (0, 0, 1, 0)$, la puntuació és la llargada del pètal i res més. Si
$w = (0.25, 0.25, 0.25, 0.25)$, és la mitjana de les quatre mesures.

Regla de les formes, que val la pena memoritzar: **(150, 4) @ (4,) -> (150,)**. El 4 del
mig es cancel·la, i el que sobreviu són les puntuacions. Si les dimensions del mig no
coincideixen, numpy peta, i gairebé sempre vol dir que algú ha oblidat una transposada.

Ho implementem dues vegades: amb dos bucles com diu la fórmula, i amb `X @ w`.
"""))

cells.append(code(r"""
np.random.seed(42)
w = np.random.randn(4)        # uns pesos qualssevol, els mateixos sempre per la llavor

print("w =", np.round(w, 6))

# versió 1: els bucles de la fórmula
n_files, n_cols = X.shape
puntuacions_bucle = np.zeros(n_files)
for i in range(n_files):
    suma = 0.0
    for j in range(n_cols):
        suma += X[i, j] * w[j]
    puntuacions_bucle[i] = suma

# versió 2: la llibreria
puntuacions_numpy = X @ w

print("Forma de X:", X.shape, " forma de w:", w.shape,
      " forma del resultat:", puntuacions_numpy.shape)
print("Primeres 5 puntuacions (bucle):", np.round(puntuacions_bucle[:5], 6))
print("Primeres 5 puntuacions (X @ w):", np.round(puntuacions_numpy[:5], 6))
print(f"Diferència màxima: {np.max(np.abs(puntuacions_bucle - puntuacions_numpy)):.2e}")
print("Coincideixen:", np.allclose(puntuacions_bucle, puntuacions_numpy))
"""))

cells.append(md(r"""
Les dues versions donen `[3.260687, 3.230476, 3.038712, 3.132405, 3.197189]` per a les
cinc primeres flors, amb una diferència màxima de `1.78e-15`. No és zero exacte perquè les
sumes es fan en ordres diferents i la coma flotant no és associativa; `1.78e-15` sobre
números de mida 3 vol dir que coincideixen fins al quinzè decimal.

`X @ w` no fa cap cosa més llesta que el bucle: fa les mateixes 600 multiplicacions. El
que canvia és que les fa dins de codi compilat en lloc de dins de l'intèrpret de Python.
Aquesta és tota la diferència, i és la raó per la qual el codi de machine learning està
escrit amb matrius i no amb bucles.
"""))

# ---------------------------------------------------------------- 7. el moment clau
cells.append(md(r"""
## 7. Un model entrenat és un vector i una multiplicació

Aquest és l'apartat pel qual existeix el quadern.

Al quadern de la regressió logística vam dir que el model calcula una puntuació i que el
signe d'aquella puntuació decideix la classe. La puntuació era això:

$$z = w_1 x_1 + w_2 x_2 + w_3 x_3 + w_4 x_4 + b$$

Això és una suma de productes més una constant, és a dir **un producte escalar més un
número**. I si en lloc d'una flor en volem les 150 alhora, és un producte matriu-vector:

$$z = Xw + b$$

La regla de decisió és el signe:

$$\hat{y} = \begin{cases} 1 & \text{si } z > 0 \\ 0 & \text{si } z < 0 \end{cases}$$

El conjunt de punts on $z = 0$ és la **frontera de decisió**. El vector $w$ és
perpendicular a aquesta frontera, i per això el producte escalar $Xw$ mesura de quina
banda cau cada punt: és la projecció de cada flor sobre la direcció $w$, desplaçada per
$b$. Tot l'apartat 5 servia per a aquesta frase.

Ho anem a comprovar de la manera més directa que hi ha: entrenem un `LogisticRegression`
de scikit-learn, li traiem els números de dins, fem el càlcul a mà i mirem si el signe
coincideix amb `model.predict` en les 150 flors.

**Una simplificació declarada:** Iris té 3 espècies i la regla del signe val per a 2
classes. Amb 3 classes, `coef_` té 3 files i la decisió no és un signe sinó un màxim entre
tres puntuacions. Per això reduïm el problema a una pregunta de sí o no: **és virgínica?**
Això no rebaixa res del que volem demostrar, i el cas de 3 classes és el mateix càlcul
repetit tres vegades amb un `argmax` al final.
"""))

cells.append(code(r"""
from sklearn.linear_model import LogisticRegression

y_binari = (y == 2).astype(int)        # 1 = virgínica, 0 = la resta

model = LogisticRegression(max_iter=1000)
model.fit(X, y_binari)

print("coef_      =", np.round(model.coef_, 6), " forma:", model.coef_.shape)
print("intercept_ =", np.round(model.intercept_, 6))
print()
print("El model entrenat, sencer:")
for nom, pes in zip(noms_mesures, model.coef_[0]):
    print(f"  {nom:12s} {pes:+.6f}")
print(f"  {'(constant)':12s} {model.intercept_[0]:+.6f}")
"""))

cells.append(md(r"""
Això és tot el que hi ha dins del model: **cinc números**. Quatre pesos i una constant. El
`fit` ha durat un moment, ha mirat 150 flors, i el resultat de tot plegat són cinc números
que caben en una línia.

Els signes ja diuen coses: els pesos del pètal són positius i grans (`+2.930641` i
`+2.416088`), els del sèpal són negatius i petits. Pètal gran empeny cap a virgínica.

Ara el càlcul a mà.
"""))

cells.append(code(r"""
w_model = model.coef_[0]          # el vector de 4 pesos
b_model = model.intercept_[0]     # la constant

z = X @ w_model + b_model         # la fórmula z = Xw + b, per a les 150 flors alhora
prediccio_a_ma = (z > 0).astype(int)

prediccio_sklearn = model.predict(X)

coincidencies = int(np.sum(prediccio_a_ma == prediccio_sklearn))
print("Forma de z:", z.shape)
print("z de les 3 primeres flors:", np.round(z[:3], 6))
print()
print(f"Files que coincideixen: {coincidencies} de {len(y)}")
print(f"Percentatge de coincidència: {100 * coincidencies / len(y):.2f} %")
print("Idèntiques:", np.array_equal(prediccio_a_ma, prediccio_sklearn))
"""))

cells.append(md(r"""
**150 de 150. El 100.00 %.**

No hi ha aproximació ni sort. `model.predict` no fa res més que aquest producte escalar i
mirar-ne el signe. De fet scikit-learn deixa el pas intermedi a la vista, i el podem
comparar amb la nostra `z`.
"""))

cells.append(code(r"""
z_sklearn = model.decision_function(X)

print("z a mà      (3 primeres):", np.round(z[:3], 6))
print("z d'sklearn (3 primeres):", np.round(z_sklearn[:3], 6))
print(f"Diferència màxima: {np.max(np.abs(z - z_sklearn)):.2e}")
print("Coincideixen:", np.allclose(z, z_sklearn))
"""))

cells.append(md(r"""
`decision_function` **és** `X @ coef_[0] + intercept_[0]`. La diferència màxima en les 150
files és `0.00e+00`: no és que s'assembli, és la mateixa operació.

Dues coses per no confondre-les:

- **Coincidir amb `predict` no vol dir encertar.** El model encerta el 97.33 % de les
  flors, perquè versicolor i virgínica es toquen. El 100 % és de la reproducció del
  càlcul, no de la classificació.
- **El que no hem fet és l'entrenament.** Hem agafat els pesos ja trobats. D'on surten
  aquests cinc números és la pregunta del quadern següent.

Dibuixem la `z` de les 150 flors. La frontera de decisió, que en 4 dimensions és un
objecte que no es pot dibuixar, en aquest gràfic és una línia horitzontal: $z = 0$.
"""))

cells.append(code(r"""
index = np.arange(len(z))

plt.figure(figsize=(8, 5))
plt.scatter(index[y_binari == 0], z[y_binari == 0],
            s=30, alpha=0.75, label="no virgínica (etiqueta real)")
plt.scatter(index[y_binari == 1], z[y_binari == 1],
            s=30, alpha=0.75, label="virgínica (etiqueta real)")
plt.axhline(0, color="black", linewidth=1.5, label="frontera de decisió (z = 0)")

plt.xlabel("Índex de la flor dins del dataset")
plt.ylabel("Puntuació z = Xw + b")
plt.title("El model redueix cada flor a un número, i el signe decideix")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
"""))

cells.append(md(r"""
Les 100 primeres flors (setosa i versicolor) tenen la `z` clarament negativa, i les 50
últimes la tenen majoritàriament positiva. Les poques que creuen la línia pel costat
equivocat són els errors del model. Els punts que queden a prop de la línia són les flors
sobre les quals el model dubta: `z` petita vol dir poca distància a la frontera.
"""))

# ---------------------------------------------------------------- 8. transposada
cells.append(md(r"""
## 8. La transposada, i per què apareix pertot

La **transposada** d'una matriu s'escriu $X^\top$ i consisteix a canviar files per
columnes:

$$(X^\top)_{ij} = X_{ji}$$

En dades vol dir canviar de pregunta. `X` és de 150 x 4: **una fila per flor.** $X^\top$
és de 4 x 150: **una fila per mesura.** La mateixa informació, ordenada per l'altra banda.
La fila 2 de $X^\top$ són les 150 llargades de pètal del dataset.

La transposada apareix pertot per una raó mecànica: el producte de matrius exigeix que les
dimensions del mig coincideixin, i quan no coincideixen la transposada és el que les fa
quadrar. El cas que veureu més és aquest:

$$X^\top X \qquad (4 \times 150) \; @ \; (150 \times 4) \;\longrightarrow\; 4 \times 4$$

El 150 es cancel·la i queda una matriu de 4 x 4: **una casella per cada parella de
mesures.** La casella $(i, j)$ és el producte escalar de la columna $i$ amb la columna $j$,
és a dir la suma sobre les 150 flors de $X_{ki} X_{kj}$. És un número que relaciona dues
mesures entre elles sobre tot el dataset.

Ho deixem aquí. Què es fa amb aquesta matriu és tema d'un altre quadern: centrant les
dades i dividint pel nombre de flors, surt la **matriu de covariància**, que és el punt de
partida del PCA. Ara ens interessa veure la forma i notar que és simètrica.
"""))

cells.append(code(r"""
print("Forma de X   :", X.shape)
print("Forma de X.T :", X.T.shape)
print()
print("Fila 2 de X.T (les llargades de pètal), primeres 8:", X.T[2][:8])
print("Columna 2 de X, primeres 8:                        ", X[:, 2][:8])
print("Són la mateixa cosa:", np.array_equal(X.T[2], X[:, 2]))

G = X.T @ X
print()
print("Forma de X.T @ X:", G.shape)
print(np.round(G, 2))
print()
print("És simètrica (G = G.T):", np.allclose(G, G.T))
print("La casella (2,2) és la suma dels quadrats de la llargada de pètal:",
      np.isclose(G[2, 2], np.sum(X[:, 2] ** 2)))
"""))

cells.append(md(r"""
La matriu surt simètrica, i té sentit: la casella $(i, j)$ i la $(j, i)$ són el mateix
producte escalar amb els factors canviats d'ordre. La diagonal són les sumes de quadrats
de cada mesura (`5223.85`, `1430.40`, `2582.71`, `302.33`), i les caselles de fora de la
diagonal relacionen parelles de mesures diferents.
"""))

# ---------------------------------------------------------------- practica
cells.append(md(r"""
## Pràctica

Quatre exercicis. Les cel·les estan buides a propòsit: el comentari diu què cal fer, i la
línia final de cada enunciat diu quin número ha de sortir, per poder-ho comprovar sols.

Teniu disponibles `X`, `y`, `iris` i `noms_mesures` de les cel·les anteriors.
"""))

cells.append(md(r"""
### Exercici 1. Manhattan contra euclidiana

La **distància de Manhattan** no eleva al quadrat ni fa cap arrel: suma les diferències en
valor absolut.

$$d_{\text{manhattan}}(a, b) = \sum_{i=1}^{n} |a_i - b_i|$$

Calculeu-la entre `X[0]` i `X[50]`, compareu-la amb la distància euclidiana de les
mateixes dues flors, i expliqueu quina de les dues és més gran i per què.

*Com sabeu que ho heu fet bé:* Manhattan ha de donar `6.7` i l'euclidiana `4.003748`.
"""))

cells.append(code(r"""
# 1. Calculeu la distància de Manhattan entre X[0] i X[50] amb np.abs i np.sum.
# 2. Calculeu la distància euclidiana de les mateixes dues flors.
# 3. Imprimiu-les totes dues i mireu quina és més gran.
"""))

cells.append(md(r"""
### Exercici 2. Les dues flors més allunyades del dataset

Trobeu la parella de flors amb la distància euclidiana més gran de tot el dataset, i
digueu de quines espècies són.

Es pot fer amb dos bucles sobre les 150 flors (22.500 parelles, que un ordinador fa sense
suar), o sense cap bucle amb `X[:, None, :] - X[None, :, :]`, que genera les 150 x 150
diferències de cop. Les dues versions valen. Si feu servir `np.argmax`, recordeu que dona
la posició dins de l'array aplanat: `np.unravel_index` la torna a convertir en fila i
columna.

*Com sabeu que ho heu fet bé:* la distància màxima és `7.085196`, entre les flors amb
índex `13` (setosa) i `118` (virgínica).
"""))

cells.append(code(r"""
# 1. Calculeu la distància euclidiana de totes les parelles de flors.
# 2. Trobeu els dos índexs on la distància és màxima.
# 3. Imprimiu la distància, els dos índexs, les seves mesures i les seves espècies.
"""))

cells.append(md(r"""
### Exercici 3. La desigualtat triangular

La norma compleix aquesta propietat, que es diu **desigualtat triangular**:

$$\|p + q\| \le \|p\| + \|q\|$$

En paraules: anar directe mai no és més llarg que fer una parada pel camí. La igualtat es
dona quan els dos vectors apunten exactament en la mateixa direcció.

Genereu dos vectors de 4 components a l'atzar amb `np.random.seed(0)` i `np.random.randn(4)`
(dues crides), comproveu la desigualtat, i després torneu-ho a provar amb `q = 3 * p` per
veure el cas d'igualtat.

*Com sabeu que ho heu fet bé:* amb la llavor 0 surt $\|p+q\| = 4.648461$ i
$\|p\| + \|q\| = 5.358619$, de manera que la desigualtat es compleix. Amb `q = 3 * p` els
dos costats han de donar el mateix número.
"""))

cells.append(code(r"""
# 1. np.random.seed(0) i genereu p i q amb np.random.randn(4).
# 2. Calculeu les tres normes: |p+q|, |p| i |q|.
# 3. Comproveu que |p+q| <= |p| + |q|.
# 4. Repetiu-ho amb q = 3 * p i mireu què passa amb la desigualtat.
"""))

cells.append(md(r"""
### Exercici 4. El bucle i el producte de matrius, amb dades inventades

A l'apartat 6 hem comprovat que `X @ w` i el bucle donen el mateix amb Iris. Comproveu-ho
ara amb dades generades a l'atzar i d'una altra mida: una matriu `A` de 200 x 5 i un vector
`w` de 5 components, amb `np.random.seed(1)`.

Escriviu la versió amb bucles i la versió amb `@`, compareu-les amb `np.allclose` i
imprimiu la diferència màxima. Mireu-vos també les formes: `(200, 5) @ (5,)` ha de donar
`(200,)`.

*Com sabeu que ho heu fet bé:* `np.allclose` ha de donar `True` i la diferència màxima ha
de ser de l'ordre de $10^{-16}$ o $10^{-15}$, mai un número gran.
"""))

cells.append(code(r"""
# 1. np.random.seed(1); A = np.random.randn(200, 5); w = np.random.randn(5).
# 2. Calculeu les 200 puntuacions amb dos bucles.
# 3. Calculeu-les amb A @ w.
# 4. Imprimiu les formes, la diferència màxima i el resultat de np.allclose.
"""))

# ---------------------------------------------------------------- resum
cells.append(md(r"""
## Resum

Què s'ha demostrat en aquest quadern, amb números a la mà:

- La **norma** feta a mà i `np.linalg.norm` donen el mateix: `6.345077` per a la flor 0.
  La norma és Pitàgoras amb $n$ sumands.
- La **distància euclidiana** del quadern de k-NN és la norma d'una diferència. El número
  entre les flors 0 i 50 és `4.003748` per les dues vies, que arrodonit és el `4.00` que ja
  teniu escrit en aquell quadern.
- Les **dues definicions del producte escalar** donen el mateix número: `6.86`, amb l'angle
  mesurat a part amb `np.arctan2`, en 2 dimensions on la comprovació no és circular. De la
  igualtat surt l'angle entre dues flors en 4 dimensions: `21.816` graus.
- **$Xw$ amb bucles i `X @ w`** coincideixen fins a `1.78e-15`. La llibreria no fa una cosa
  diferent; fa el mateix més de pressa.
- **La predicció de la regressió logística és `X @ w + b` i un signe.** El càlcul a mà
  coincideix amb `model.predict` en `150 de 150` files, el `100.00 %`, i la nostra `z` és
  idèntica a `model.decision_function(X)` amb diferència `0.00e+00`. El model entrenat són
  quatre pesos i una constant.

La conseqüència, dita sense adornos: quan feu `fit`, el que passa és que es busquen uns
números; quan feu `predict`, el que passa és una multiplicació. No hi ha res més a dins.

## I ara què

Queda la pregunta que aquest quadern ha deixat oberta a propòsit: **d'on surten els
pesos.** Hem agafat els cinc números ja trobats i hem verificat que fan la feina, però no
hem vist com es troben.

Això és `MA_02_descens_gradient.ipynb`, on es veurà que trobar-los és baixar per un pendent
a passes petites, i que el pendent es calcula amb les mateixes eines d'aquest quadern.
"""))


if __name__ == "__main__":
    print(escriu(cells, DESTI, titol_colab="MA_01_algebra_lineal.ipynb"))
