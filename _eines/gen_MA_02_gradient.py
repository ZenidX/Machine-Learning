# -*- coding: utf-8 -*-
"""Genera el quadern MA_02: descens de gradient.

Desfa la trampa de ML_04 (buscar els pesos per forca bruta) i construeix el
descens de gradient des de zero: derivada, descens en 1D, gradient en diverses
dimensions, log-loss, la seva derivada, gradient checking, entrenament sencer a
ma i comparacio amb scikit-learn.

    python _eines/gen_MA_02_gradient.py
"""
import sys

sys.path.insert(0, "_eines")

from nbgen import md, code, escriu

cells = []
A = cells.append

# ---------------------------------------------------------------- portada
A(md(r"""
# Descens de gradient

**Optativa d'Aprenentatge automàtic · DAM/DAW 2n**

Al quadern `ML_04_regressio_logistica.ipynb` vam trobar els pesos d'una regressió
logística **provant-los tots**: una graella de 60 × 60 valors de $w_1$ i $w_2$, calcular
la pèrdua a cada punt i quedar-nos el millor. Allà ho vam titular «sense derivades», i
era una trampa deliberada: servia per veure el paisatge de la pèrdua sense haver
d'explicar càlcul.

Aquest quadern desfà la trampa. Primer veurem per què la força bruta no escala (i el
número que surt és desagradable), i després construirem el mecanisme que fan servir de
debò tots els models que s'entrenen: **el descens de gradient**.

No heu fet càlcul mai. Tot el que faci falta de derivades el muntem aquí des de zero.
No està rebaixat: el que farem al final del quadern és el mateix que fa
`LogisticRegression` per dins, i ho comprovarem número a número.
"""))

A(code(r'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

np.random.seed(42)

# Les mateixes dades de ML_04: versicolor contra virginica, amb les dues
# columnes del petal.
iris = load_iris(as_frame=True)
dades = iris.frame.copy()
dades["especie"] = iris.target_names[iris.target]
dades = dades.rename(columns={
    "sepal length (cm)": "sepal_llarg",
    "sepal width (cm)": "sepal_ample",
    "petal length (cm)": "petal_llarg",
    "petal width (cm)": "petal_ample",
})

bi = dades[dades["especie"].isin(["versicolor", "virginica"])].copy()
bi["y"] = (bi["especie"] == "virginica").astype(int)   # 0 = versicolor, 1 = virginica
colors_bi = {"versicolor": "tab:orange", "virginica": "tab:green"}

X = bi[["petal_llarg", "petal_ample"]].values
y = bi["y"].values

# Mateixa divisio que a ML_04: mateix test_size, mateix random_state, mateix stratify.
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

print(f"Entrenament: {Xtr.shape[0]} flors, {Xtr.shape[1]} columnes")
print(f"Examen:      {Xte.shape[0]} flors")


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


EPS = 1e-12   # per que hi es, a la seccio 5


def log_loss(w, b, X, y):
    """Perdua logaritmica (log-loss) d'uns pesos w i un biaix b sobre (X, y)."""
    p = sigmoide(X @ w + b)
    p = np.clip(p, EPS, 1 - EPS)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
'''))

# ---------------------------------------------------------------- 1
A(md(r"""
## 1. Per què la força bruta no serveix

### 1.1 El que vam fer a ML_04

A ML_04 vam fixar el biaix $b$ i vam recórrer una graella de 60 valors de $w_1$ per 60
valors de $w_2$, tots dos entre 0 i 5. Són 3.600 combinacions, i a cadascuna vam calcular
la pèrdua. Reproduïm exactament aquell càlcul i mirem-ne dues coses que allà no vam dir:
**quin és el millor punt de la graella** i **quina resolució té**.
"""))

A(code(r'''
# El biaix que vam fixar a ML_04: el que havia trobat scikit-learn.
model_sk = LogisticRegression(random_state=42)
model_sk.fit(Xtr, ytr)
b_fixat = model_sk.intercept_[0]

w1_vals = np.linspace(0, 5, 60)
w2_vals = np.linspace(0, 5, 60)
W1, W2 = np.meshgrid(w1_vals, w2_vals)

L_graella = np.zeros_like(W1)
for i in range(W1.shape[0]):
    for j in range(W1.shape[1]):
        L_graella[i, j] = log_loss(np.array([W1[i, j], W2[i, j]]), b_fixat, Xtr, ytr)

k = np.unravel_index(np.argmin(L_graella), L_graella.shape)
w1_graella, w2_graella = W1[k], W2[k]
L_millor_graella = L_graella[k]

print(f"Avaluacions de la perdua: {L_graella.size}")
print(f"Pas de la graella: {w1_vals[1] - w1_vals[0]:.4f}")
print(f"Millor punt de la graella: w1 = {w1_graella:.4f}, w2 = {w2_graella:.4f}")
print(f"Perdua en aquest punt: {L_millor_graella:.6f}")
print(f"w2 es al limit de la graella? {w2_graella == w2_vals[-1]}")
'''))

A(md(r"""
Dues coses incòmodes, i totes dues són defectes del mètode i no de les dades:

- El millor punt de la graella té $w_2 = 5{,}0000$, que és **el límit de la graella**.
  Vol dir que el mínim de veritat cau fora de la caixa que hem mirat. La graella no ha
  trobat el fons de la vall: ha trobat el punt més baix de la paret.
- La resolució és de 0,0847 per pes. Qualsevol cosa més fina que això és invisible per a
  la graella, i el biaix $b$ no l'hem buscat: l'hem copiat de scikit-learn, que és una
  manera elegant de dir que aquella part del problema la vam saltar.

### 1.2 Què passa si afegim pesos

La graella de ML_04 tenia 60 valors per pes i 2 pesos. Posem-hi 100 valors per pes, que
tampoc és cap luxe, i comptem combinacions segons el nombre de pesos $d$:

$$\text{combinacions} = 100^d$$

Amb 2 pesos són $100^2$. Amb 4, $100^4$. El conjunt de dades de càncer de mama que fem
servir a la pràctica té 30 columnes, és a dir 30 pesos: $100^{30}$.
"""))

A(code(r'''
for d in [2, 3, 4, 10, 30]:
    print(f"{d:>3} pesos -> {100 ** d:,} combinacions")

combinacions_30 = 100 ** 30
print(f"\nAmb 30 pesos, el numero exacte te {len(str(combinacions_30))} digits:")
print(combinacions_30)
'''))

A(md(r"""
Un número amb 61 dígits no diu gran cosa per si sol. Posem-lo en temps: mesurem quant
triga **una sola** avaluació de la pèrdua sobre el conjunt de càncer (569 files, 30
columnes) i multipliquem.
"""))

A(code(r'''
import time

cancer = load_breast_cancer()
Xc, yc = cancer.data, cancer.target
print(f"Conjunt de cancer: {Xc.shape[0]} files, {Xc.shape[1]} columnes")

w_zero = np.zeros(Xc.shape[1])
t0 = time.perf_counter()
REPETICIONS = 2000
for _ in range(REPETICIONS):
    log_loss(w_zero, 0.0, Xc, yc)
per_avaluacio = (time.perf_counter() - t0) / REPETICIONS
print(f"Temps d'una avaluacio de la perdua: {per_avaluacio:.2e} s")

edat_univers_s = 13.8e9 * 365.25 * 24 * 3600   # ~13.800 milions d'anys, en segons

for d in [2, 4, 30]:
    segons = (100.0 ** d) * per_avaluacio
    if segons < 60:
        quant = f"{segons:.1f} segons"
    elif segons < 3600 * 24 * 365:
        quant = f"{segons / 60:.0f} minuts"
    else:
        quant = f"{segons / edat_univers_s:.2e} vegades l'edat de l'univers"
    print(f"{d:>3} pesos: {100.0 ** d:.0e} avaluacions -> {quant}")
'''))

A(md(r"""
Aquest és el número que justifica tot el quadern. Amb 4 pesos la força bruta ja costa
de l'ordre d'una hora. Amb els 30 pesos del conjunt de càncer costa de l'ordre de $10^{37}$ vegades
l'edat de l'univers, i això suposant que tinguéssiu tots els ordinadors del món i que
cap no s'espatllés. Al vostre ordinador el número sortirà una mica diferent, $10^{36}$ o
$10^{38}$, i és igual: cap factor de deu no arregla això.

I fixeu-vos que 30 columnes és un problema **petit**. Una xarxa neuronal de les que fan
servir avui té entre milions i bilions de pesos.

La conclusió és que provar valors no és una estratègia. Cal poder mirar el paisatge de la
pèrdua **en un sol punt** i, des d'aquell punt, saber cap a on baixa. Això és exactament
el que fa una derivada.
"""))

# ---------------------------------------------------------------- 2
A(md(r"""
## 2. Què és una derivada

### 2.1 El pendent d'una recta

D'una recta ja en sabeu calcular el pendent: agafeu dos punts i dividiu el que puja entre
el que avança.

$$m = \frac{f(x_2) - f(x_1)}{x_2 - x_1}$$

A una recta aquest número surt igual tant li fa quins dos punts agafeu. Comprovem-ho amb
$f(x) = 3x + 1$.
"""))

A(code(r'''
def recta(x):
    return 3 * x + 1


parelles = [(0.0, 1.0), (-2.0, 5.0), (10.0, 10.5), (1.0, 1.0001)]
for x1, x2 in parelles:
    m = (recta(x2) - recta(x1)) / (x2 - x1)
    print(f"x1={x1:>6}, x2={x2:>8}  ->  pendent = {m:.6f}")
'''))

A(md(r"""
### 2.2 El pendent d'una corba en un punt

A una corba això ja no funciona, perquè el pendent canvia a cada lloc. Si agafeu dos punts
allunyats, el que obteniu és el pendent mitjà entre tots dos, no el pendent **en un punt**.

L'arreglada és aquesta: agafeu el segon punt cada vegada més a prop del primer. Amb
$x_2 = x + h$, el quocient queda

$$\frac{f(x+h) - f(x)}{h}$$

i el pendent en el punt $x$ és el número cap al qual tendeix aquest quocient quan $h$ es
fa cada vegada més petita. Això és la **derivada**, i s'escriu

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

El símbol $\lim_{h \to 0}$ no és una divisió per zero: és «cap a quin número s'acosta això
si faig $h$ tan petita com vulgui». La divisió per zero no es fa mai.

Amb paper i llapis es demostra que per a $f(x) = x^2$ la derivada és $f'(x) = 2x$. Nosaltres
no ho demostrarem: ho **comprovarem numèricament**, posant una $h$ petita i mirant si surt
$2x$.
"""))

A(code(r'''
def f(x):
    return x ** 2


h = 1e-5
punts = np.array([-2.0, -0.5, 0.0, 1.0, 1.5, 3.0])

derivada_numerica = (f(punts + h) - f(punts)) / h
derivada_exacta = 2 * punts

taula = pd.DataFrame({
    "x": punts,
    "quocient (h=1e-5)": derivada_numerica,
    "2x": derivada_exacta,
    "diferencia": np.abs(derivada_numerica - derivada_exacta),
})
print(taula.to_string(index=False, float_format=lambda v: f"{v:.8f}"))
print(f"\nDiferencia maxima: {np.abs(derivada_numerica - derivada_exacta).max():.2e}")
'''))

A(md(r"""
Coincideix amb $2x$ amb cinc decimals bons. La diferència que queda, $10^{-5}$, és
exactament de l'ordre de la $h$ que hem posat: no és soroll, és que el quocient amb una
$h$ finita és una aproximació de la derivada i l'error baixa proporcionalment a $h$.

Hi ha una variant que costa el mateix i és molt millor, la **diferència centrada**: mirar
un pas cap endavant i un cap enrere en lloc de només endavant.

$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$
"""))

A(code(r'''
centrada = (f(punts + h) - f(punts - h)) / (2 * h)
print(f"Diferencia maxima amb la formula endavant: {np.abs(derivada_numerica - 2 * punts).max():.2e}")
print(f"Diferencia maxima amb la formula centrada: {np.abs(centrada - 2 * punts).max():.2e}")
'''))

A(md(r"""
De $10^{-5}$ a $10^{-11}$ pel mateix preu. La farem servir a la secció 7, quan haguem de
verificar un gradient de debò.

### 2.3 La derivada, dibuixada

La derivada en un punt és el pendent de la **recta tangent** a la corba en aquell punt. La
recta tangent que passa per $(x_0, f(x_0))$ amb pendent $f'(x_0)$ és

$$t(x) = f(x_0) + f'(x_0)\,(x - x_0)$$
"""))

A(code(r'''
x0 = 1.5
pendent_x0 = (f(x0 + h) - f(x0 - h)) / (2 * h)

xs = np.linspace(-3, 3, 300)
tangent = f(x0) + pendent_x0 * (xs - x0)

plt.figure(figsize=(7, 5))
plt.plot(xs, f(xs), color="tab:blue", linewidth=2, label="$f(x) = x^2$")
plt.plot(xs, tangent, color="tab:red", linestyle="--", linewidth=1.5,
         label=f"tangent a $x_0={x0}$, pendent {pendent_x0:.2f}")
plt.scatter([x0], [f(x0)], color="black", zorder=5)
plt.ylim(-2, 9)
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.title("La derivada es el pendent de la recta tangent")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
### 2.4 Una $h$ massa petita tampoc no va bé

La teoria diu $h \to 0$. L'ordinador no fa límits: fa restes amb números de 64 bits. Si
$h$ és molt petita, $f(x+h)$ i $f(x)$ són gairebé el mateix número, la resta perd gairebé
tots els dígits significatius i el resultat es degrada. Mireu l'error en funció de $h$.
"""))

A(code(r'''
hs = np.array([1e-1, 1e-2, 1e-3, 1e-5, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16])
errors = np.abs((f(1.5 + hs) - f(1.5)) / hs - 3.0)

for hh, er in zip(hs, errors):
    print(f"h = {hh:.0e}   error = {er:.3e}")

plt.figure(figsize=(7, 4.5))
plt.loglog(hs, errors, "o-", color="tab:purple")
plt.xlabel("$h$")
plt.ylabel("error respecte de $f'(1{,}5) = 3$")
plt.title("La derivada numerica te una h optima")
plt.grid(alpha=0.3, which="both")
plt.show()
'''))

A(md(r"""
La corba baixa, toca fons a prop de $h = 10^{-8}$ i torna a pujar. La baixada és l'error
de l'aproximació (com més petita la $h$, millor); la pujada és l'error de la màquina
arrodonint restes de números gairebé iguals. Amb $h = 10^{-16}$ l'error és pitjor que amb
$h = 10^{-1}$.

Ho expliquem perquè és una cosa real de la pràctica i perquè a la secció 7 haurem de
triar una $h$ concreta. No és una curiositat: és el motiu pel qual no es deriven les
funcions numèricament quan es pot fer amb una fórmula.

### 2.5 La lectura que ens importa

Tot això no ho volem per saber pendents. Ho volem per una cosa molt més concreta:

- Si $f'(x) > 0$, la funció **puja** cap a la dreta. Per fer baixar $f$, cal moure $x$ cap
  a l'**esquerra**.
- Si $f'(x) < 0$, la funció **baixa** cap a la dreta. Per fer baixar $f$, cal moure $x$ cap
  a la **dreta**.
- Si $f'(x) = 0$, en aquell punt la funció és plana: no hi ha direcció de baixada.

En els tres casos, moure's **en sentit contrari al signe de la derivada** fa baixar $f$.
Aquesta frase és tot el descens de gradient. Amb una derivada, calculada en un sol punt,
ja sabem cap a on anar, i no hem hagut de provar cap graella.
"""))

# ---------------------------------------------------------------- 3
A(md(r"""
## 3. Descens de gradient en una dimensió

La regla, escrita sencera:

$$x \leftarrow x - \eta \, f'(x)$$

La fletxa vol dir «substitueix el valor de $x$ pel que hi ha a la dreta». El número
$\eta$ (la lletra grega *eta*) es diu **taxa d'aprenentatge** i diu com de llarga és la
passa. El signe menys és la conclusió de la secció 2.4: ens movem contra el signe de la
derivada.

Provem-ho sobre $f(x) = x^2$, sortint de $x_0 = 3$, amb $\eta = 0{,}1$. La derivada la
posem exacta, $f'(x) = 2x$, perquè aquesta ja la sabem.
"""))

A(code(r'''
def descens_1d(x0, eta, passos):
    """Aplica x <- x - eta*f'(x) sobre f(x)=x^2 i retorna tota la trajectoria."""
    x = x0
    trajectoria = [x]
    for _ in range(passos):
        derivada = 2 * x          # f'(x) = 2x
        x = x - eta * derivada
        trajectoria.append(x)
    return np.array(trajectoria)


traj = descens_1d(3.0, eta=0.1, passos=40)

for i in range(6):
    print(f"pas {i}:  x = {traj[i]:.6f}   f(x) = {traj[i] ** 2:.6f}")
print("...")
print(f"pas 40: x = {traj[-1]:.6e}   f(x) = {traj[-1] ** 2:.6e}")
'''))

A(md(r"""
Cada passa multiplica $x$ per $1 - 2\eta = 0{,}8$: $3 \to 2{,}4 \to 1{,}92 \to 1{,}536
\to \ldots$ Al pas 40 ja som a $3{,}99 \cdot 10^{-4}$, i el mínim de $x^2$ és a $x = 0$.
No hi arriba mai exactament, s'hi acosta tant com vulgueu. Això és normal i és el que
passa també quan s'entrena un model de debò.
"""))

A(code(r'''
xs = np.linspace(-3.4, 3.4, 300)

plt.figure(figsize=(7, 5))
plt.plot(xs, f(xs), color="tab:blue", linewidth=2, label="$f(x) = x^2$")
plt.plot(traj, traj ** 2, "o-", color="tab:red", markersize=5, linewidth=1,
         label=r"trajectoria, $\eta = 0{,}1$")
plt.scatter([traj[0]], [traj[0] ** 2], color="black", zorder=5, s=70, label="sortida")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.title("Descens de gradient baixant per la corba")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
Les passes són llargues a dalt i curtes a baix, i no perquè ho haguem programat: a prop
del mínim la derivada és petita, i la passa val $\eta$ multiplicat per la derivada. El
mètode frena sol quan arriba.

### 3.1 La taxa d'aprenentatge

$\eta$ és l'única cosa que hem triat a mà, i tria el destí del mètode. Sobre $f(x)=x^2$ es
pot veure exactament què passa: cada passa multiplica $x$ per $1 - 2\eta$.

- $\eta = 0{,}1$: factor $0{,}8$. Cada passa acosta. Convergeix.
- $\eta = 0{,}01$: factor $0{,}98$. També acosta, però tan poc que 40 passes no arriben.
- $\eta = 1{,}01$: factor $-1{,}02$. La passa passa de llarg del mínim i cau més amunt del
  que era. **Divergeix**: cada vegada més lluny, amb el signe alternat.

Dibuixem els tres casos junts. Posem $|x_k|$ en escala logarítmica a l'eix vertical,
perquè si no el cas que divergeix aixafa els altres dos.
"""))

A(code(r'''
plt.figure(figsize=(7.5, 5))
for eta, color in [(0.1, "tab:green"), (0.01, "tab:orange"), (1.01, "tab:red")]:
    t = descens_1d(3.0, eta=eta, passos=40)
    plt.semilogy(np.abs(t), "o-", markersize=3.5, color=color,
                 label=rf"$\eta = {eta}$   ($|x_{{40}}| = {abs(t[-1]):.3g}$)")

plt.xlabel("nombre de passes")
plt.ylabel("$|x_k|$ (escala logaritmica)")
plt.title("La taxa d'aprenentatge decideix si el metode funciona")
plt.legend()
plt.grid(alpha=0.3, which="both")
plt.show()
'''))

A(md(r"""
La línia verda baixa recta cap a zero. La taronja baixa amb el mateix pendent però tan a
poc a poc que al pas 40 encara és a 1,34. La vermella **puja**.

No hi ha manera de saber la $\eta$ bona a priori. Per a $f(x)=x^2$ es pot calcular que cal
$\eta < 1$; per a una funció qualsevol, es prova. Un senyal fiable: si la pèrdua puja en
lloc de baixar, la $\eta$ és massa gran.
"""))

# ---------------------------------------------------------------- 4
A(md(r"""
## 4. El gradient, amb més d'una variable

Un model té molts pesos, i la pèrdua és una funció de tots alhora. Amb dues variables,
$f(x, y)$, hi ha dues preguntes de pendent en cada punt: com canvia $f$ si movem $x$
deixant $y$ quieta, i com canvia si movem $y$ deixant $x$ quieta. Cadascuna és una
**derivada parcial**, i s'escriuen amb la lletra $\partial$:

$$\frac{\partial f}{\partial x}(x, y) = \lim_{h \to 0} \frac{f(x+h,\, y) - f(x,\, y)}{h}
\qquad
\frac{\partial f}{\partial y}(x, y) = \lim_{h \to 0} \frac{f(x,\, y+h) - f(x,\, y)}{h}$$

És la mateixa definició de la secció 2, amb la resta de variables tractades com a
constants. El **gradient** és el vector que les posa totes juntes:

$$\nabla f(x, y) = \left( \frac{\partial f}{\partial x},\ \frac{\partial f}{\partial y} \right)$$

El símbol $\nabla$ es llegeix «nabla». Amb $d$ variables el gradient és un vector de $d$
números, un per variable.

Prenem $f(x, y) = x^2 + 3y^2$. Derivant respecte de $x$, el terme $3y^2$ és una constant i
desapareix; derivant respecte de $y$, desapareix $x^2$:

$$\nabla f(x, y) = (2x,\ 6y)$$

Comprovem-ho numèricament abans de fer-nos-en confiança.
"""))

A(code(r'''
def g(v):
    x, y = v
    return x ** 2 + 3 * y ** 2


def grad_g(v):
    x, y = v
    return np.array([2 * x, 6 * y])


def gradient_numeric(func, v, h=1e-6):
    """Gradient per diferencies centrades, component a component."""
    v = np.asarray(v, dtype=float)
    g_num = np.zeros_like(v)
    for j in range(len(v)):
        pas = np.zeros_like(v)
        pas[j] = h
        g_num[j] = (func(v + pas) - func(v - pas)) / (2 * h)
    return g_num


for punt in [np.array([1.0, 1.0]), np.array([2.5, 1.8]), np.array([-3.0, 0.5])]:
    analitic = grad_g(punt)
    numeric = gradient_numeric(g, punt)
    print(f"punt {punt}:  analitic {analitic}  numeric {np.round(numeric, 6)}  "
          f"dif max {np.abs(analitic - numeric).max():.2e}")
'''))

A(md(r"""
La regla de descens és **la mateixa**, però amb vectors. On abans hi havia un número ara
hi ha un vector, i on hi havia la derivada ara hi ha el gradient:

$$\mathbf{v} \leftarrow \mathbf{v} - \eta \, \nabla f(\mathbf{v})$$

En NumPy això és una resta de vectors i prou. Dibuixem-ho: les corbes de nivell de
$f(x,y) = x^2 + 3y^2$ (el conjunt de punts on $f$ val el mateix, com un mapa topogràfic) i
la trajectòria a sobre.
"""))

A(code(r'''
v = np.array([2.5, 1.8])
eta = 0.1
traj_2d = [v.copy()]
for _ in range(25):
    v = v - eta * grad_g(v)
    traj_2d.append(v.copy())
traj_2d = np.array(traj_2d)

print(f"Sortida: {traj_2d[0]}")
print(f"Pas 25:  {traj_2d[-1]}")
print(f"f a la sortida: {g(traj_2d[0]):.4f}   f al pas 25: {g(traj_2d[-1]):.3e}")

xg = np.linspace(-3, 3, 200)
yg = np.linspace(-2.2, 2.2, 200)
XG, YG = np.meshgrid(xg, yg)
ZG = XG ** 2 + 3 * YG ** 2

plt.figure(figsize=(7.5, 5.5))
cs = plt.contourf(XG, YG, ZG, levels=25, cmap="viridis")
plt.colorbar(cs, label="$f(x, y) = x^2 + 3y^2$")
plt.contour(XG, YG, ZG, levels=12, colors="white", linewidths=0.5, alpha=0.6)
plt.plot(traj_2d[:, 0], traj_2d[:, 1], "o-", color="tab:red", markersize=4,
         linewidth=1.2, label="trajectoria del descens")
plt.scatter([traj_2d[0, 0]], [traj_2d[0, 1]], color="black", s=70, zorder=5,
            label="sortida")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("El descens creua les corbes de nivell perpendicularment")
plt.legend()
plt.show()
'''))

A(md(r"""
Dues coses per llegir al gràfic:

- La trajectòria **talla les corbes de nivell en angle recte**. No és casualitat: al llarg
  d'una corba de nivell $f$ no canvia, i la direcció on $f$ canvia més de pressa és
  justament la perpendicular. El gradient apunta sempre cap a la pujada més forta, i
  nosaltres anem en el sentit contrari.
- El moviment vertical s'acaba molt abans que l'horitzontal. El factor $3$ del terme
  $3y^2$ fa que la derivada respecte de $y$ sigui tres vegades més gran, i amb la mateixa
  $\eta$ la component $y$ es menja el camí de pressa (al pas 25 val $2 \cdot 10^{-10}$)
  mentre la $x$ encara és a $9{,}4 \cdot 10^{-3}$.

Aquesta segona observació és un problema real i té nom: **mal condicionament**. Quan les
variables tenen escales molt diferents, una $\eta$ que va bé per a una va malament per a
l'altra. Ens hi tornarem a trobar a la secció 8, amb les columnes del pètal.
"""))

# ---------------------------------------------------------------- 5
A(md(r"""
## 5. La funció que minimitza la regressió logística

Ja tenim el mecanisme. Ara cal la funció a la qual aplicar-lo.

El model és el de ML_04: per a cada flor $i$, amb les seves columnes al vector $x_i$,

$$z_i = x_i \cdot w + b, \qquad p_i = \sigma(z_i) = \frac{1}{1 + e^{-z_i}}$$

i la funció de pèrdua és la **log-loss** o **entropia creuada binària**:

$$L(w, b) = -\frac{1}{n}\sum_{i=1}^{n}\Big[ y_i \log p_i + (1 - y_i) \log(1 - p_i) \Big]$$

Cada $y_i$ val 0 o 1, de manera que a cada suma un dels dos termes sempre s'anul·la: si
$y_i = 1$ el terme que queda és $\log p_i$, i si $y_i = 0$ és $\log(1 - p_i)$. Escrit
així, amb els dos termes i un multiplicador que val 0 o 1, no cal cap `if` i la fórmula
és una operació de vectors.

### 5.1 Per què aquesta i no el nombre d'errors

La pregunta és raonable: el que volem és encertar, i el que compta els encerts és el
nombre d'errors. Per què no minimitzar-lo directament?

Perquè el nombre d'errors **és un esglaó**. Mireu-lo per a un sol exemple amb $y = 1$:
val 1 mentre $p < 0{,}5$ i val 0 a partir d'allà. És pla a l'esquerra, pla a la dreta, i
salta al mig. La seva derivada és zero a tot arreu on existeix, i on saltaria no
existeix. Un gradient de zero no diu cap a on anar: el mètode de la secció 3 es queda
quiet on sigui.

La log-loss d'aquell mateix exemple és $-\log p$, que baixa suaument cap a 0 quan $p$
s'acosta a 1 i es dispara quan $p$ s'acosta a 0. Té pendent a tot arreu, i el pendent
apunta cap a on cal anar encara que la predicció ja sigui correcta.
"""))

A(code(r'''
ps = np.linspace(0.001, 0.999, 400)
perdua_log = -np.log(ps)               # log-loss d'un exemple amb y = 1
perdua_errors = (ps < 0.5).astype(float)   # nombre d'errors del mateix exemple

plt.figure(figsize=(7.5, 5))
plt.plot(ps, perdua_log, color="tab:blue", linewidth=2,
         label=r"log-loss: $-\log p$")
plt.plot(ps, perdua_errors, color="tab:red", linewidth=2,
         label="nombre d'errors: 1 si $p < 0{,}5$")
plt.ylim(-0.2, 4)
plt.xlabel("$p$, probabilitat que dona el model")
plt.ylabel("perdua de l'exemple")
plt.title("Perdua d'un sol exemple amb etiqueta real $y = 1$")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
La corba blava té pendent a cada punt i el pendent sempre empeny cap a la dreta, cap a
$p$ més gran. La vermella és plana, plana, i un salt. Comprovem que el seu gradient és
zero de debò, mesurant-lo amb la fórmula centrada de la secció 2 sobre el nombre d'errors
de tot el conjunt d'entrenament.
"""))

A(code(r'''
def perdua_errors_totals(w, b, X, y):
    """Proporcio de flors mal classificades. El que voldriem minimitzar."""
    prediccio = (sigmoide(X @ w + b) >= 0.5).astype(int)
    return np.mean(prediccio != y)


w_prova = np.array([2.5, 2.2])
b_prova = -15.8

grad_errors = gradient_numeric(
    lambda v: perdua_errors_totals(v, b_prova, Xtr, ytr), w_prova, h=1e-6)
grad_logloss = gradient_numeric(
    lambda v: log_loss(v, b_prova, Xtr, ytr), w_prova, h=1e-6)

print(f"Errors al punt de prova: {perdua_errors_totals(w_prova, b_prova, Xtr, ytr):.4f}")
print(f"Gradient del nombre d'errors: {grad_errors}")
print(f"Gradient de la log-loss:      {np.round(grad_logloss, 6)}")

# I ara un punt triat a mala fe: amb w = (2, 2) i b = -15, tres flors cauen
# EXACTAMENT sobre la ratlla (z = 0), i moure els pesos una mil.lionesima les fa
# canviar de banda.
z_dolent = Xtr @ np.array([2.0, 2.0]) + (-15.0)
print(f"\nFlors amb z = 0 exacte al punt (2, 2, -15): {(z_dolent == 0).sum()}")
print("Gradient del nombre d'errors aqui: "
      f"{gradient_numeric(lambda v: perdua_errors_totals(v, -15.0, Xtr, ytr), np.array([2.0, 2.0]))}")
'''))

A(md(r"""
El gradient del nombre d'errors és `[0. 0.]` exactament: moure els pesos una mil·lionèsima
no fa canviar de banda cap flor, i per tant el comptador no es mou. El de la log-loss dona
números que no són zero i que apunten a alguna banda. La log-loss no és una aproximació
dolenta del nombre d'errors: és la funció que **es pot derivar**, i aquesta és tota la
raó per la qual es fa servir.

La segona part de la cel·la ensenya l'altra cara del problema, i és pitjor que el zero. Al
punt $(2,\ 2,\ -15)$ hi ha tres flors del conjunt d'entrenament que cauen exactament sobre
la ratlla, i allà el quocient incremental dona $-21.429$, un número enorme i sense cap
sentit: no és cap pendent, és un salt dividit per $2h$. Un esglaó no té derivada zero a tot
arreu; té derivada zero a tot arreu **on existeix**, i on no existeix el càlcul numèric
retorna el que li surti. Cap de les dues coses serveix per decidir cap a on moure's.

### 5.2 El `eps` dins del logaritme

$\log(0)$ és $-\infty$. Si el model arriba a donar una probabilitat de 0 exacta a una flor
que és de la classe 1, la pèrdua val infinit, el gradient val `nan` i a partir d'allà tot
el que calculeu són `nan`, sense cap missatge que digui on ha començat el problema.

I passa de debò: $\sigma(z)$ en aritmètica de 64 bits arriba a 0,0 exacta a partir de
$z \approx -745$, i a 1,0 exacta a partir de $z \approx +37$. No fa falta cap error de
programació, n'hi ha prou amb pesos grans.

L'arreglada és la línia que hi ha a `log_loss` des de la primera cel·la:

```python
p = np.clip(p, EPS, 1 - EPS)   # EPS = 1e-12
```

Retallar les probabilitats dins de l'interval $[10^{-12},\ 1 - 10^{-12}]$. No canvia res
del que ens interessa (un $10^{-12}$ no mou cap decimal que llegirem) i evita l'infinit.
Això no és una elegància teòrica: és una cosa que es posa a tot el codi de producció, i el
dia que no hi és us el trobareu depurant `nan`.
"""))

A(code(r'''
# np.errstate(...) calla els avisos de numpy. Aqui ho fem a proposit, perque
# provoquem l'error expressament; al vostre codi de debo, l'avis el voleu veure.
with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
    print(f"sigmoide(-745) = {sigmoide(-745.0)}")
    print(f"sigmoide(-800) = {sigmoide(-800.0)}   <- zero exacte")
    print(f"sigmoide(38)   = {sigmoide(38.0)}     <- un exacte")

    amb_clip = log_loss(np.array([0.0, 0.0]), -800.0, Xtr, ytr)
    p_cru = sigmoide(Xtr @ np.array([0.0, 0.0]) + (-800.0))
    sense_clip = -np.mean(ytr * np.log(p_cru) + (1 - ytr) * np.log(1 - p_cru))

print(f"\nPerdua amb clip:  {amb_clip:.4f}")
print(f"Perdua sense clip: {sense_clip}")
'''))

# ---------------------------------------------------------------- 6
A(md(r"""
## 6. La derivada de la log-loss

Ara toca derivar la log-loss respecte de cada pes. Farem servir tres regles de càlcul que
us donem sense demostrar, i ho diem clarament perquè quedi marcat el que ens saltem:

1. La derivada d'una suma és la suma de les derivades, i les constants multiplicatives
   surten fora.
2. $\dfrac{d}{du} \log u = \dfrac{1}{u}$.
3. **Regla de la cadena**: si una quantitat depèn de $u$ i $u$ depèn de $v$, els pendents
   es multipliquen: $\dfrac{d}{dv} = \dfrac{d}{du} \cdot \dfrac{du}{dv}$.

La regla de la cadena és la important. Diu que si moure $v$ una mica mou $u$ el doble, i
moure $u$ una mica mou el resultat el triple, aleshores moure $v$ mou el resultat sis
vegades més.

### 6.1 Primer, la derivada de la sigmoide

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Amb la regla de la cadena i sabent que la derivada de $e^{-z}$ és $-e^{-z}$:

$$\sigma'(z) = -\frac{1}{(1 + e^{-z})^2} \cdot (-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}$$

I ara el detall que fa bonic tot el que ve després. Com que

$$1 - \sigma(z) = 1 - \frac{1}{1 + e^{-z}} = \frac{e^{-z}}{1 + e^{-z}}$$

el producte $\sigma(z)\,(1 - \sigma(z))$ val

$$\frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \frac{e^{-z}}{(1 + e^{-z})^2}$$

que és exactament el que acabàvem d'obtenir. Per tant

$$\boxed{\sigma'(z) = \sigma(z)\,\big(1 - \sigma(z)\big)}$$

La derivada de la sigmoide s'escriu amb la sigmoide mateixa. Comprovem-ho abans de
continuar.
"""))

A(code(r'''
zs = np.array([-5.0, -2.0, -0.5, 0.0, 0.5, 2.0, 5.0])

sigma_prima_numerica = (sigmoide(zs + 1e-6) - sigmoide(zs - 1e-6)) / (2e-6)
sigma_prima_formula = sigmoide(zs) * (1 - sigmoide(zs))

taula = pd.DataFrame({
    "z": zs,
    "numerica": sigma_prima_numerica,
    "sigma(z)(1-sigma(z))": sigma_prima_formula,
    "diferencia": np.abs(sigma_prima_numerica - sigma_prima_formula),
})
print(taula.to_string(index=False, float_format=lambda v: f"{v:.10f}"))
print(f"\nDiferencia maxima: {np.abs(sigma_prima_numerica - sigma_prima_formula).max():.2e}")
'''))

A(md(r"""
### 6.2 La derivació, pas a pas

Anem a buscar $\dfrac{\partial L}{\partial w_j}$. La cadena de dependències és aquesta:
$w_j$ mou $z_i$, $z_i$ mou $p_i$, i $p_i$ mou la pèrdua. Recorrem-la a l'inrevés.

**Pas 1.** Derivem el terme de dins respecte de $p_i$. Diem
$\ell_i = y_i \log p_i + (1 - y_i)\log(1 - p_i)$. Amb la regla del logaritme i la de la
cadena aplicada a $\log(1 - p_i)$ (la derivada de $1 - p_i$ respecte de $p_i$ és $-1$):

$$\frac{\partial \ell_i}{\partial p_i} = \frac{y_i}{p_i} - \frac{1 - y_i}{1 - p_i}$$

**Pas 2.** De $p_i$ a $z_i$ ja ho tenim de la secció 6.1:
$\dfrac{\partial p_i}{\partial z_i} = p_i (1 - p_i)$.

**Pas 3.** Els multipliquem, que és la regla de la cadena, i mireu què passa:

$$\frac{\partial \ell_i}{\partial z_i}
= \left( \frac{y_i}{p_i} - \frac{1 - y_i}{1 - p_i} \right) p_i (1 - p_i)
= y_i (1 - p_i) - (1 - y_i)\, p_i$$

Els denominadors $p_i$ i $1 - p_i$ s'han cancel·lat contra el factor $p_i(1-p_i)$ que
venia de la sigmoide. Desenvolupant el que queda:

$$y_i - y_i p_i - p_i + y_i p_i = y_i - p_i$$

**Pas 4.** La pèrdua és $L = -\frac{1}{n}\sum_i \ell_i$, amb el signe menys i l'$\frac1n$
al davant:

$$\frac{\partial L}{\partial z_i} = -\frac{1}{n}\,(y_i - p_i) = \frac{1}{n}\,(p_i - y_i)$$

**Pas 5.** Falta anar de $z_i$ a $w_j$. Com que $z_i = \sum_j x_{ij} w_j + b$, mou $w_j$
una unitat i $z_i$ es mou $x_{ij}$ unitats:

$$\frac{\partial z_i}{\partial w_j} = x_{ij}, \qquad \frac{\partial z_i}{\partial b} = 1$$

**Pas 6.** Cadena una última vegada i sumem sobre totes les flors:

$$\frac{\partial L}{\partial w_j} = \frac{1}{n}\sum_{i=1}^{n} (p_i - y_i)\, x_{ij},
\qquad
\frac{\partial L}{\partial b} = \frac{1}{n}\sum_{i=1}^{n} (p_i - y_i)$$

I això, escrit amb matrius, és

$$\nabla_w L = \frac{1}{n} X^\top (p - y), \qquad
\frac{\partial L}{\partial b} = \frac{1}{n} \mathbf{1}^\top (p - y)$$

### 6.3 Què vol dir el resultat

Val la pena aturar-se aquí, perquè el resultat és desproporcionadament net per a la feina
que hem fet.

Tota la derivada de la log-loss és **la matriu de dades transposada multiplicada pel
vector d'errors**. Res d'exponencials, res de logaritmes: han desaparegut tots per la
cancel·lació del pas 3. El vector $p - y$ és l'error de cada flor, amb signe: positiu si
el model s'ha passat de probabilitat, negatiu si s'ha quedat curt.

Component a component: $\dfrac{\partial L}{\partial w_j}$ és el producte escalar de la
columna $j$ de les dades amb el vector d'errors, dividit per $n$. El pes d'una columna es
mou en proporció a com de correlacionada està aquella columna amb l'error que el model
comet ara mateix. Si una columna no té res a veure amb els errors, el seu pes no es mou.

En codi és una línia:

```python
grad = X.T @ (p - y) / n
```

Un últim detall que sortirà a la secció 8: la derivada respecte de $b$ és la **mitjana de
l'error**. Al mínim val zero, i per tant al mínim la mitjana de les probabilitats que
dona el model és igual a la proporció real de la classe 1. És una propietat que podrem
comprovar.

També cal dir el que això no és: si la pèrdua fos l'error quadràtic
$\frac1n\sum (p_i - y_i)^2$ en lloc de la log-loss, el factor $p_i(1-p_i)$ del pas 3 no es
cancel·laria i sobreviuria al gradient. Aquell factor val gairebé zero quan $p_i$ és a
prop de 0 o de 1, de manera que una flor de la qual el model està **molt segur i
equivocat** no generaria gairebé cap gradient i el model no aprendria d'ella. La log-loss
és l'única pèrdua que fa desaparèixer aquest factor. No és casualitat que sigui la que es
fa servir.
"""))

A(code(r'''
def gradient(w, b, X, y):
    """Gradient analitic de la log-loss. Les dues linies del pas 6."""
    p = sigmoide(X @ w + b)
    grad_w = X.T @ (p - y) / len(y)
    grad_b = np.mean(p - y)
    return grad_w, grad_b


g_w, g_b = gradient(np.array([0.7, -0.4]), 0.2, Xtr, ytr)
print(f"gradient respecte de w: {g_w}")
print(f"gradient respecte de b: {g_b:.8f}")
'''))

# ---------------------------------------------------------------- 7
A(md(r"""
## 7. Comprovar que la derivada és correcta (*gradient checking*)

Hem derivat sis passos a mà. Un error de signe o un factor $n$ perdut donaria un codi que
corre, que no peta i que entrena malament, i costa molt de trobar mirant-lo.

Hi ha una manera de verificar-ho que no depèn de si la derivació és bona, i és comparar el
gradient analític amb el **gradient numèric** calculat component a component amb
diferències centrades, la fórmula de la secció 2.2:

$$\frac{\partial L}{\partial w_j} \approx \frac{L(w + h e_j) - L(w - h e_j)}{2h}$$

on $e_j$ és el vector que val 1 a la posició $j$ i 0 a la resta: moure **un sol** pes i
deixar els altres quiets. Això té nom propi, *gradient checking*, i és el que es fa sempre
que s'implementa un gradient nou. Costa $2d$ avaluacions de la pèrdua, massa car per
entrenar, però es fa un cop i es guarda la tranquil·litat.

La $h$ la posem a $10^{-6}$, prop del fons de la corba de la secció 2.4.
"""))

A(code(r'''
w_test = np.array([0.7, -0.4])
b_test = 0.2
h_gc = 1e-6

grad_w_analitic, grad_b_analitic = gradient(w_test, b_test, Xtr, ytr)

# numeric respecte de cada component de w
grad_w_numeric = np.zeros_like(w_test)
for j in range(len(w_test)):
    e_j = np.zeros_like(w_test)
    e_j[j] = h_gc
    grad_w_numeric[j] = (log_loss(w_test + e_j, b_test, Xtr, ytr)
                         - log_loss(w_test - e_j, b_test, Xtr, ytr)) / (2 * h_gc)

# numeric respecte de b
grad_b_numeric = (log_loss(w_test, b_test + h_gc, Xtr, ytr)
                  - log_loss(w_test, b_test - h_gc, Xtr, ytr)) / (2 * h_gc)

comprovacio = pd.DataFrame({
    "parametre": ["w1", "w2", "b"],
    "analitic": [grad_w_analitic[0], grad_w_analitic[1], grad_b_analitic],
    "numeric": [grad_w_numeric[0], grad_w_numeric[1], grad_b_numeric],
})
comprovacio["diferencia"] = np.abs(comprovacio["analitic"] - comprovacio["numeric"])
print(comprovacio.to_string(index=False, float_format=lambda v: f"{v:.12f}"))

dif_maxima = comprovacio["diferencia"].max()
print(f"\nDiferencia maxima: {dif_maxima:.3e}")
print("Gradient verificat." if dif_maxima < 1e-7 else "MALAMENT: reviseu la derivacio.")
'''))

A(md(r"""
Coincideixen fins al desè decimal: la diferència màxima és de l'ordre de
$1{,}3 \cdot 10^{-10}$, i el que en queda és l'error de la diferència centrada, no un
error de la derivació. Amb això ja podem confiar en `gradient()`.

El criteri habitual és exigir una diferència per sota de $10^{-7}$. Si surt de l'ordre de
$10^{-2}$, la derivació té un error de debò; si surt de l'ordre de $10^{-5}$, mireu-vos
primer la $h$.
"""))

# ---------------------------------------------------------------- 8
A(md(r"""
## 8. Entrenar la regressió logística sencera, a mà

Ja tenim totes les peces. El bucle d'entrenament és:

1. Començar amb $w = (0, 0)$ i $b = 0$.
2. Calcular les probabilitats $p = \sigma(Xw + b)$.
3. Calcular el gradient amb la fórmula verificada.
4. Restar-lo, multiplicat per $\eta$.
5. Tornar al 2.

Res més. Les vuit línies de `entrena()` són tot l'entrenament d'una regressió logística.
Guardem la pèrdua a cada iteració per poder-la dibuixar.

Sobre els números que hem triat: $\eta = 0{,}5$ i 20.000 iteracions. Són moltes, i el
motiu és el mal condicionament de la secció 4. La llargada del pètal va de 3 a 7 cm i
l'amplada d'1 a 2,5: les dues columnes tenen escales diferents, el paisatge de la pèrdua
és una vall allargada i estreta, i el descens hi baixa de biaix. A la pràctica això es
resol **normalitzant les columnes** abans d'entrenar, i no ho farem aquí perquè volem
pesos comparables amb els de ML_04 i amb els de scikit-learn, que estan en les unitats
originals.
"""))

A(code(r'''
def entrena(X, y, eta, iteracions):
    """Descens de gradient sobre la log-loss. Retorna pesos, biaix i historial."""
    w = np.zeros(X.shape[1])
    b = 0.0
    historial = []
    for _ in range(iteracions):
        historial.append(log_loss(w, b, X, y))
        grad_w, grad_b = gradient(w, b, X, y)
        w = w - eta * grad_w
        b = b - eta * grad_b
    historial.append(log_loss(w, b, X, y))
    return w, b, np.array(historial)


w_gd, b_gd, historial = entrena(Xtr, ytr, eta=0.5, iteracions=20000)

print(f"Perdua a la iteracio 0:     {historial[0]:.6f}")
print(f"Perdua a la iteracio 20000: {historial[-1]:.6f}\n")
print(f"w1 = {w_gd[0]:.4f}")
print(f"w2 = {w_gd[1]:.4f}")
print(f"b  = {b_gd:.4f}")

p_tr = sigmoide(Xtr @ w_gd + b_gd)
print(f"\nMitjana de l'error (p - y): {np.mean(p_tr - ytr):.6f}")
print(f"Mitjana de p: {p_tr.mean():.6f}   proporcio real de virginica: {ytr.mean():.6f}")
'''))

A(md(r"""
La pèrdua ha baixat de 0,693147 a 0,072547. El valor de sortida no és casual: amb
$w = 0$ i $b = 0$ totes les probabilitats valen 0,5, i $-\log(0{,}5) = 0{,}6931$. Sempre
que comenceu de zero, la pèrdua inicial serà aquest número.

La mitjana de l'error val $9{,}2 \cdot 10^{-4}$, pràcticament zero, i la mitjana de les
probabilitats (0,500921) coincideix amb la proporció de virginica del conjunt
d'entrenament (0,5 exacte, perquè el `stratify` ha repartit 35 i 35). És la
propietat de la secció 6.3: el gradient del biaix és la mitjana de l'error, i si el
descens ha arribat a baix, aquesta mitjana ha d'estar a prop de zero. Que surti confirma
que el bucle fa el que hem derivat.
"""))

A(code(r'''
plt.figure(figsize=(7.5, 5))
plt.plot(historial, color="tab:blue", linewidth=1.8)
plt.xlabel("iteracio")
plt.ylabel("perdua (log-loss) a l'entrenament")
plt.title(r"La perdua baixant, $\eta = 0{,}5$")
plt.grid(alpha=0.3)
plt.show()

plt.figure(figsize=(7.5, 5))
plt.semilogx(np.arange(1, len(historial) + 1), historial, color="tab:blue", linewidth=1.8)
plt.xlabel("iteracio (escala logaritmica)")
plt.ylabel("perdua (log-loss) a l'entrenament")
plt.title("La mateixa corba, amb l'eix horitzontal logaritmic")
plt.grid(alpha=0.3, which="both")
plt.show()
'''))

A(md(r"""
El primer gràfic té un problema de lectura: la pèrdua cau tant a les primeres iteracions
que la resta de la corba sembla plana i no s'hi veu res. El segon és el mateix amb l'eix
horitzontal logarítmic, i ara sí que es veu que continua baixant fins al final. Aquesta és
la manera habitual de mirar una corba de pèrdua i val la pena agafar el costum.
"""))

# ---------------------------------------------------------------- 9
A(md(r"""
## 9. Comparació amb scikit-learn

Entrenem un `LogisticRegression` amb les mateixes dades i posem els pesos costat a costat.
"""))

A(code(r'''
model_C1 = LogisticRegression(random_state=42)                      # C = 1, el valor per defecte
model_C1.fit(Xtr, ytr)

comparacio = pd.DataFrame({
    "nostre (gradient, 20000 it.)": [w_gd[0], w_gd[1], b_gd,
                                     log_loss(w_gd, b_gd, Xtr, ytr)],
    "scikit-learn (C=1)": [model_C1.coef_[0][0], model_C1.coef_[0][1],
                           model_C1.intercept_[0],
                           log_loss(model_C1.coef_[0], model_C1.intercept_[0], Xtr, ytr)],
}, index=["w1", "w2", "b", "log-loss a l'entrenament"])
print(comparacio.to_string(float_format=lambda v: f"{v:.4f}"))
'''))

A(md(r"""
No s'assemblen gens: $w_2$ ens surt 11,44 i a ells 2,22. I tanmateix la nostra log-loss és
més baixa que la seva, 0,0725 contra 0,1735.

Això últim és la pista. Si els nostres pesos donen menys pèrdua que els seus i ells diuen
haver trobat el mínim, el que minimitzen no pot ser la mateixa funció. I no ho és:
`LogisticRegression` minimitza, per defecte,

$$\frac{1}{2} w^\top w + C \sum_{i=1}^{n} \big[ \text{log-loss de la flor } i \big]$$

és a dir, la pèrdua **més un terme que penalitza els pesos grans**. Això es diu
**regularització**, i el paràmetre $C$ en controla la força: com més petit és $C$, més pesa
la penalització i més frenats queden els pesos. Amb $C = 1$, el que hi ha per defecte, el
fre és considerable.

Dividint aquella expressió per $C \cdot n$ (dividir per una constant positiva no canvia on
és el mínim), la funció de scikit-learn es pot escriure com la nostra més un terme:

$$L(w, b) + \lambda \| w \|^2, \qquad \lambda = \frac{1}{2 C n}$$

Per acostar els resultats hi ha, doncs, dos camins. El primer és treure'ls la
regularització posant una $C$ molt gran.
"""))

A(code(r'''
model_Cgran = LogisticRegression(C=1e6, max_iter=10000, random_state=42)
model_Cgran.fit(Xtr, ytr)

# El nostre descens, pero deixant-lo baixar de debo: mes iteracions i eta mes gran.
w_llarg, b_llarg, hist_llarg = entrena(Xtr, ytr, eta=2.0, iteracions=200000)

comparacio2 = pd.DataFrame({
    "nostre (200000 it., eta=2)": [w_llarg[0], w_llarg[1], b_llarg,
                                   log_loss(w_llarg, b_llarg, Xtr, ytr)],
    "scikit-learn (C=1e6)": [model_Cgran.coef_[0][0], model_Cgran.coef_[0][1],
                             model_Cgran.intercept_[0],
                             log_loss(model_Cgran.coef_[0], model_Cgran.intercept_[0],
                                      Xtr, ytr)],
}, index=["w1", "w2", "b", "log-loss a l'entrenament"])
print(comparacio2.to_string(float_format=lambda v: f"{v:.4f}"))

print(f"\nlog-loss nostra:       {log_loss(w_llarg, b_llarg, Xtr, ytr):.8f}")
print(f"log-loss scikit-learn: "
      f"{log_loss(model_Cgran.coef_[0], model_Cgran.intercept_[0], Xtr, ytr):.8f}")
print(f"\nDiferencia relativa maxima als pesos: "
      f"{np.abs(np.append(w_llarg, b_llarg) / np.append(model_Cgran.coef_[0], model_Cgran.intercept_[0]) - 1).max():.2%}")
print(f"Iteracions que ha fet scikit-learn: {model_Cgran.n_iter_[0]}")
print(f"Iteracions que hem fet nosaltres:   200000")
'''))

A(md(r"""
Ara sí. Els pesos coincideixen amb una diferència relativa de l'ordre del 0,1 % i la
log-loss coincideix fins al sisè decimal, 0,065354 tots dos. Els dos mètodes han arribat al
mateix punt.

Queden dues diferències petites, i totes dues tenen explicació:

- Els pesos no són idèntics fins a l'últim decimal perquè cap dels dos mètodes hi ha
  arribat exactament. El fons d'aquesta vall és molt pla i molt llarg (recordeu el mal
  condicionament), i tant les nostres 200.000 iteracions com el criteri d'aturada de
  scikit-learn s'aturen a prop, no a sobre.
- `LogisticRegression` no fa descens de gradient. Per defecte fa servir **L-BFGS**, un
  mètode que estima també la curvatura de la funció i fa passes adaptades a cada direcció,
  i per això li calen 27 iteracions on nosaltres n'hem fet 200.000. La idea de baixar pel
  pendent és la mateixa; el que canvia és com de llesta és cada passa.

El segon camí per acostar-los és el contrari: afegir la regularització al **nostre**
gradient. Derivant $\lambda \|w\|^2 = \lambda \sum_j w_j^2$ respecte de $w_j$ surt
$2\lambda w_j$, de manera que tot el canvi és sumar $2\lambda w$ al gradient dels pesos (i
res al del biaix: el biaix no es penalitza).
"""))

A(code(r'''
def entrena_regularitzat(X, y, eta, iteracions, lam):
    """Igual que entrena(), pero minimitzant log-loss + lam*||w||^2."""
    w = np.zeros(X.shape[1])
    b = 0.0
    for _ in range(iteracions):
        grad_w, grad_b = gradient(w, b, X, y)
        w = w - eta * (grad_w + 2 * lam * w)     # el terme nou
        b = b - eta * grad_b                     # el biaix no es penalitza
    return w, b


lam = 1 / (2 * 1.0 * len(ytr))       # lambda = 1/(2*C*n) amb C = 1
print(f"lambda equivalent a C=1: {lam:.6f}\n")

w_reg, b_reg = entrena_regularitzat(Xtr, ytr, eta=0.5, iteracions=50000, lam=lam)

comparacio3 = pd.DataFrame({
    "nostre + lambda*||w||^2": [w_reg[0], w_reg[1], b_reg],
    "scikit-learn (C=1)": [model_C1.coef_[0][0], model_C1.coef_[0][1],
                           model_C1.intercept_[0]],
}, index=["w1", "w2", "b"])
print(comparacio3.to_string(float_format=lambda v: f"{v:.4f}"))
print(f"\nDiferencia maxima: "
      f"{np.abs(comparacio3.iloc[:, 0] - comparacio3.iloc[:, 1]).max():.2e}")
'''))

A(md(r"""
Amb el terme de regularització afegit, el nostre descens troba els pesos de scikit-learn
amb $C=1$ fins al quart decimal: 2,4668 i 2,2156, biaix $-15{,}8323$. Els mateixos
números. La diferència de la primera taula no era cap misteri de la implementació: era una
funció objectiu diferent, i ara que minimitzem la mateixa funció surt el mateix resultat.

### 9.1 Les prediccions

Els pesos es poden veure molt diferents i les prediccions ser gairebé les mateixes: el que
decideix la classe és el signe de $x \cdot w + b$, i multiplicar $w$ i $b$ tots dos per
tres no canvia cap signe. Mirem quantes flors classifiquen igual.
"""))

A(code(r'''
def prediu(w, b, X):
    return (sigmoide(X @ w + b) >= 0.5).astype(int)


pred_nostre = prediu(w_gd, b_gd, X)              # les 100 flors
pred_C1 = model_C1.predict(X)
pred_Cgran = model_Cgran.predict(X)
pred_llarg = prediu(w_llarg, b_llarg, X)

for nom, altra in [("scikit-learn C=1", pred_C1), ("scikit-learn C=1e6", pred_Cgran)]:
    coincid = (pred_nostre == altra).sum()
    print(f"nostre (20000 it.) contra {nom:<20}: {coincid}/100 = {coincid / 100:.1%}")

coincid = (pred_llarg == pred_Cgran).sum()
print(f"nostre (200000 it.) contra scikit-learn C=1e6 : {coincid}/100 = {coincid / 100:.1%}")

print("\nPrecisio sobre les 30 flors de l'examen:")
print(f"  nostre (20000 it.):    {(prediu(w_gd, b_gd, Xte) == yte).mean():.1%}")
print(f"  nostre (200000 it.):   {(prediu(w_llarg, b_llarg, Xte) == yte).mean():.1%}")
print(f"  scikit-learn C=1:      {model_C1.score(Xte, yte):.1%}")
print(f"  scikit-learn C=1e6:    {model_Cgran.score(Xte, yte):.1%}")
'''))

A(md(r"""
Amb els pesos de 20.000 iteracions coincidim amb scikit-learn per defecte en **94 de les
100 flors**, tot i que els pesos són cinc vegades més grans; amb $C=10^6$ hi coincidim en
98. I els nostres pesos de 200.000 iteracions coincideixen amb els de $C=10^6$ en les 100
flors, cosa que ja esperàvem perquè són pràcticament el mateix vector.

La precisió a l'examen diu una altra cosa que val la pena no amagar: nosaltres fem 86,7 %
i scikit-learn amb $C=1$ fa 93,3 %. Els nostres pesos donen menys pèrdua a l'entrenament i
alhora encerten menys a l'examen. Això és **sobreajustament**, i és exactament el que la
regularització serveix per evitar. Dit d'una altra manera: minimitzar la pèrdua
d'entrenament fins al fons no és el que volem, i el valor per defecte $C=1$ de
scikit-learn no és cap detall menor.

Dibuixem les dues fronteres per veure-ho.
"""))

A(code(r'''
plt.figure(figsize=(8, 5.5))
for especie, grup in bi.groupby("especie"):
    plt.scatter(grup["petal_llarg"], grup["petal_ample"], label=especie,
                color=colors_bi[especie], s=40, alpha=0.8)

x1 = np.linspace(bi["petal_llarg"].min() - 0.3, bi["petal_llarg"].max() + 0.3, 100)
plt.plot(x1, -(w_gd[0] * x1 + b_gd) / w_gd[1], "k--", linewidth=2,
         label="el nostre descens (20000 it.)")
plt.plot(x1, -(model_C1.coef_[0][0] * x1 + model_C1.intercept_[0]) / model_C1.coef_[0][1],
         color="tab:purple", linestyle="-", linewidth=2,
         label="scikit-learn ($C=1$)")

plt.ylim(bi["petal_ample"].min() - 0.3, bi["petal_ample"].max() + 0.3)
plt.xlabel("Llargada del petal (cm)")
plt.ylabel("Amplada del petal (cm)")
plt.title("Les dues fronteres de decisio")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
'''))

A(md(r"""
Les dues rectes passen gairebé pel mateix lloc i tenen pendents diferents. Amb pesos que
es diferencien en un factor cinc, la frontera es mou poc: per això les prediccions
coincideixen en el 94 % dels casos mentre les taules de pesos semblen incomparables.
"""))

# ---------------------------------------------------------------- 10
A(md(r"""
## 10. Tornem a la força bruta

Falta tancar el cercle. Comparem el que va trobar la graella de ML_04 amb el que ha trobat
el gradient, i comptem què ha costat cada cosa.

Per comparar de manera justa, entrenem també amb el biaix **fixat** al mateix valor que la
graella, perquè la graella no el buscava.
"""))

A(code(r'''
def entrena_b_fixat(X, y, b, eta, iteracions, objectiu=None):
    """Descens sobre w amb b fixat. Diu a quina iteracio baixa de `objectiu`."""
    w = np.zeros(X.shape[1])
    primera_millor = None
    for i in range(1, iteracions + 1):
        p = sigmoide(X @ w + b)
        w = w - eta * (X.T @ (p - y) / len(y))
        if objectiu is not None and primera_millor is None:
            if log_loss(w, b, X, y) < objectiu:
                primera_millor = i
    return w, primera_millor


w_bfix, iteracio_batuda = entrena_b_fixat(Xtr, ytr, b_fixat, eta=0.5, iteracions=20000,
                                          objectiu=L_millor_graella)

resum = pd.DataFrame([
    {"metode": "graella 60x60 (ML_04)",
     "avaluacions": L_graella.size,
     "w1": w1_graella, "w2": w2_graella, "b": b_fixat,
     "log-loss": L_millor_graella},
    {"metode": f"gradient, b fixat, {iteracio_batuda} it.",
     "avaluacions": iteracio_batuda,
     "w1": np.nan, "w2": np.nan, "b": b_fixat,
     "log-loss": L_millor_graella},
    {"metode": "gradient, b fixat, 20000 it.",
     "avaluacions": 20000,
     "w1": w_bfix[0], "w2": w_bfix[1], "b": b_fixat,
     "log-loss": log_loss(w_bfix, b_fixat, Xtr, ytr)},
    {"metode": "gradient, tot lliure, 20000 it.",
     "avaluacions": 20000,
     "w1": w_gd[0], "w2": w_gd[1], "b": b_gd,
     "log-loss": log_loss(w_gd, b_gd, Xtr, ytr)},
])
print(resum.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

print(f"\nEl gradient baixa del millor punt de la graella a la iteracio {iteracio_batuda}.")
print(f"La graella havia gastat {L_graella.size} avaluacions per arribar-hi.")
'''))

A(md(r"""
Amb el biaix fixat igual que la graella, el gradient **passa per davant del millor punt de
tota la graella a la iteració 603**, havent mirat el paisatge en 603 punts en lloc de
3.600. I si el deixem córrer fins a 20.000 arriba a una pèrdua de 0,1205, que la graella no
pot assolir de cap manera: el seu mínim era 0,1358 i estava a la paret de la caixa.

Amb el biaix lliure, que és el problema de debò, el gradient arriba a 0,0725. La graella
no podia ni plantejar-s'ho: hauria necessitat una tercera dimensió, i $60^3 = 216.000$
avaluacions per tenir la mateixa resolució grollera.

Dibuixem-ho tot junt.
"""))

A(code(r'''
# Paisatge de la perdua amb b fixat, en una finestra mes ampla que la graella de ML_04.
w1_ample = np.linspace(-1, 6, 140)
w2_ample = np.linspace(0, 10, 140)
WA1, WA2 = np.meshgrid(w1_ample, w2_ample)
LA = np.zeros_like(WA1)
for i in range(WA1.shape[0]):
    for j in range(WA1.shape[1]):
        LA[i, j] = log_loss(np.array([WA1[i, j], WA2[i, j]]), b_fixat, Xtr, ytr)

# trajectoria del descens amb b fixat, guardant-la sencera
w_tr = np.zeros(2)
cami = [w_tr.copy()]
for _ in range(20000):
    p = sigmoide(Xtr @ w_tr + b_fixat)
    w_tr = w_tr - 0.5 * (Xtr.T @ (p - ytr) / len(ytr))
    cami.append(w_tr.copy())
cami = np.array(cami)

plt.figure(figsize=(8, 6))
cs = plt.contourf(WA1, WA2, LA, levels=30, cmap="viridis")
plt.colorbar(cs, label="perdua (log-loss)")
plt.plot([0, 5, 5, 0, 0], [0, 0, 5, 5, 0], color="white", linewidth=2,
         label="la graella de ML_04 (3600 punts)")
plt.plot(cami[:, 0], cami[:, 1], color="tab:red", linewidth=2,
         label="cami del descens de gradient")
plt.scatter([w1_graella], [w2_graella], color="white", marker="s", s=90, zorder=5,
            edgecolors="black", label="millor punt de la graella")
plt.scatter([cami[-1, 0]], [cami[-1, 1]], color="tab:red", marker="*", s=220, zorder=5,
            edgecolors="black", label="on arriba el gradient")
plt.xlabel("$w_1$ (pes de la llargada del petal)")
plt.ylabel("$w_2$ (pes de l'amplada del petal)")
plt.title("La caixa que vam mirar a ML_04 i el cami que fa el gradient")
plt.legend(loc="upper left", fontsize=9)
plt.show()
'''))

A(md(r"""
El quadrat blanc és tota la graella de ML_04: 3.600 punts repartits per aquella caixa. El
seu millor punt (el quadre amb vora negra) és a la vora de dalt, perquè la vall continua
cap amunt i la caixa la talla. La línia vermella és el descens, que surt de l'origen,
travessa la caixa i se'n va fora a buscar el fons.

Dues advertències sobre el gràfic, perquè no us endugueu una idea falsa:

- El paisatge dibuixat té $b$ fixat a $-15{,}8323$. El descens de la secció 8 mou també el
  biaix, i el seu camí de debò va per un espai de tres dimensions que no es pot dibuixar
  així. Aquesta figura és la versió de dues dimensions, comparable amb ML_04.
- La graella no és ximple per estar mal col·locada: és ximple perquè **cal saber on
  col·locar-la**, i per saber-ho ja hauríeu de conèixer la resposta. El gradient no ho
  necessita: surt d'on sigui i baixa.

I el número que importa: aquí la graella gasta $60^2$ avaluacions i el gradient unes
centenars. Amb 30 pesos, la graella gasta $100^{30}$ i el gradient gasta **les mateixes
20.000 iteracions**, perquè cada iteració calcula les 30 derivades parcials de cop amb un
sol producte de matrius. El cost del gradient creix linealment amb el nombre de pesos; el
de la força bruta, exponencialment. Aquesta és tota la diferència, i és la raó per la qual
es pot entrenar un model de mil milions de pesos i no se'n pot entrenar cap de trenta per
força bruta.
"""))

# ---------------------------------------------------------------- practica
A(md(r"""
## 11. Pràctica

### Exercici 1 — El descens sobre una altra funció

Implementa el descens de gradient sobre $f(x) = (x - 3)^2 + 2$. La derivada la pots
calcular amb la regla de la cadena ($f'(x) = 2(x-3)$) o numèricament amb diferències
centrades, com vulguis. Surt de $x_0 = 0$, fes 50 passes amb $\eta = 0{,}1$ i dibuixa la
trajectòria sobre la corba.

**Com saps que ho has fet bé:** el mínim de $f$ és a $x = 3$ i val 2. Al pas 50 hauries de
tenir $x \approx 2{,}99996$ i $f(x) \approx 2{,}0000$. Si $x$ se'n va cap a l'infinit,
t'has deixat el signe menys de la regla.
"""))

A(code(r'''
# Exercici 1
# 1. Defineix f(x) = (x-3)**2 + 2 i la seva derivada f'(x) = 2*(x-3).
# 2. Escriu el bucle: x = x - eta * derivada(x), 50 vegades, amb eta = 0.1 i x0 = 0.
# 3. Guarda tots els valors de x en una llista.
# 4. Dibuixa la corba amb plt.plot i la trajectoria a sobre amb plt.plot(xs, f(xs), "o-").
# 5. Imprimeix el valor final de x i de f(x).
'''))

A(md(r"""
### Exercici 2 — Tres taxes d'aprenentatge

Entrena la regressió logística amb `entrena(Xtr, ytr, eta, 2000)` per a
$\eta \in \{0{,}01,\ 0{,}1,\ 1{,}0\}$ i dibuixa les tres corbes de pèrdua al mateix gràfic,
amb l'eix horitzontal logarítmic. Quina arriba més avall en 2.000 iteracions? Prova també
$\eta = 3$ i mira si la corba encara baixa sempre o si fa dents de serra.

**Com saps que ho has fet bé:** a la iteració 2.000 la pèrdua hauria de ser
aproximadament 0,53 amb $\eta = 0{,}01$, 0,24 amb $\eta = 0{,}1$ i 0,095 amb
$\eta = 1{,}0$. Les tres corbes han de començar totes a 0,6931.
"""))

A(code(r'''
# Exercici 2
# 1. Per a cada eta de [0.01, 0.1, 1.0]:
#      w, b, hist = entrena(Xtr, ytr, eta, 2000)
#      plt.semilogx(hist, label=f"eta = {eta}")
# 2. Etiqueta els eixos en catala i posa la llegenda.
# 3. Imprimeix hist[0] i hist[-1] de cada cas.
# 4. Repeteix-ho amb eta = 3 i mira la forma de la corba.
'''))

A(md(r"""
### Exercici 3 — El terme de regularització

Fes servir `entrena_regularitzat()` amb $\lambda \in \{0,\ 0{,}001,\ 0{,}01,\ 0{,}1\}$
(20.000 iteracions, $\eta = 0{,}5$) i fes una taula amb els pesos i la norma
$\|w\| = \sqrt{w_1^2 + w_2^2}$ (`np.linalg.norm(w)`) de cada cas. Dibuixa la norma en
funció de $\lambda$.

**Com saps que ho has fet bé:** amb $\lambda = 0$ la norma val ≈ 11,81; amb
$\lambda = 0{,}01$ baixa a ≈ 2,93 amb pesos $w \approx (2{,}22,\ 1{,}91)$, molt a prop dels
de scikit-learn per defecte; amb $\lambda = 0{,}1$ cau a ≈ 0,97. La norma ha de baixar
sempre que $\lambda$ pugi.
"""))

A(code(r'''
# Exercici 3
# 1. Per a cada lam de [0.0, 0.001, 0.01, 0.1]:
#      w, b = entrena_regularitzat(Xtr, ytr, eta=0.5, iteracions=20000, lam=lam)
#      guarda lam, w[0], w[1], b, np.linalg.norm(w) en una llista de diccionaris
# 2. Construeix un pd.DataFrame amb la llista i imprimeix-lo.
# 3. Dibuixa la norma de w en funcio de lambda (prova plt.semilogx si es veu malament).
'''))

A(md(r"""
### Exercici 4 — Les quatre columnes d'Iris

Entrena el mateix descens de gradient però amb les **quatre** columnes d'Iris
(`sepal_llarg`, `sepal_ample`, `petal_llarg`, `petal_ample`) en lloc de les dues del
pètal. Fes servir la mateixa divisió (`test_size=0.3`, `random_state=42`,
`stratify=y`) i verifica el gradient amb *gradient checking* abans d'entrenar, ara amb
quatre components.

Fixa't que no has de canviar ni `gradient()` ni `entrena()`: la fórmula
$\frac1n X^\top (p - y)$ ja funciona amb qualsevol nombre de columnes.

**Com saps que ho has fet bé:** el *gradient checking* ha de donar una diferència màxima
per sota de $10^{-8}$ a les quatre components. Amb $\eta = 0{,}5$ i 20.000 iteracions la
pèrdua d'entrenament hauria de baixar fins a ≈ 0,066 i la precisió a l'examen hauria de
ser del 93,3 % (28 de 30), millor que el 86,7 % que fèiem amb dues columnes.
"""))

A(code(r'''
# Exercici 4
# 1. X4 = bi[["sepal_llarg", "sepal_ample", "petal_llarg", "petal_ample"]].values
# 2. X4tr, X4te, y4tr, y4te = train_test_split(X4, y, test_size=0.3,
#                                              random_state=42, stratify=y)
# 3. Gradient checking amb un w de 4 components (per exemple np.array([0.5, -0.5, 0.5, -0.5])):
#    compara gradient(...) amb el numeric component a component, com a la seccio 7.
# 4. w4, b4, hist4 = entrena(X4tr, y4tr, eta=0.5, iteracions=20000)
# 5. Imprimeix els pesos, la perdua final i la precisio a l'examen amb prediu(w4, b4, X4te).
'''))

# ---------------------------------------------------------------- resum
A(md(r"""
## Resum

- La força bruta de ML_04 no era una simplificació didàctica: era un mètode que **no
  existeix**. Amb 30 pesos i 100 valors per pes calen $100^{30}$ avaluacions, de l'ordre de
  $10^{37}$ vegades l'edat de l'univers.
- Una **derivada** és el límit del quocient incremental, i el que ens en interessa és el
  signe: moure's en sentit contrari al signe de la derivada fa baixar la funció. Ho hem
  comprovat numèricament sobre $x^2$, amb cinc decimals bons.
- El **descens de gradient**, $x \leftarrow x - \eta f'(x)$, baixa amb la informació d'un
  sol punt. La taxa $\eta$ decideix si convergeix, si va massa a poc a poc o si divergeix,
  i ho hem vist en els tres casos.
- Amb més variables, el **gradient** és el vector de derivades parcials i la regla és la
  mateixa amb vectors. El camí talla les corbes de nivell perpendicularment.
- La **log-loss** es fa servir perquè es pot derivar. El nombre d'errors té gradient
  exactament `[0. 0.]`, i ho hem mesurat.
- La derivada de la log-loss surt $\nabla_w L = \frac1n X^\top (p - y)$: la matriu de dades
  transposada pel vector d'errors. Tots els logaritmes i exponencials es cancel·len al pas
  3 de la derivació.
- L'hem **verificada** contra el gradient numèric component a component (*gradient
  checking*): diferència màxima $1{,}3 \cdot 10^{-10}$.
- Entrenant a mà hem baixat la pèrdua de 0,693147 a 0,072547, i deixant-lo córrer hem
  arribat als mateixos pesos que `LogisticRegression` amb $C = 10^6$: $(6{,}09,\ 14{,}51)$
  amb biaix $-54{,}11$, amb la mateixa pèrdua fins al sisè decimal. Afegint
  $\lambda \|w\|^2$ amb $\lambda = 1/(2Cn)$ hem reproduït els pesos de $C = 1$ fins al
  quart decimal.

### Simplificacions que hem fet i que cal saber

- No hem demostrat cap regla de derivació: la del logaritme, la de l'exponencial i la de
  la cadena les hem donades fetes. Sí que hem demostrat $\sigma' = \sigma(1-\sigma)$ i hem
  derivat la log-loss sencera.
- No hem dit res de per què el descens troba el mínim **global** i no un mínim local
  qualsevol. En aquest problema hi arriba perquè la log-loss de la regressió logística és
  convexa (té un sol fons), i això no ho hem demostrat. Amb una xarxa neuronal deixa de ser
  cert, i el mètode continua funcionant prou bé, que és una de les coses més estranyes del
  camp.
- No hem normalitzat les columnes, i per això ens calen desenes de milers d'iteracions on
  scikit-learn en gasta 27. A la pràctica es normalitza sempre.
- Hem calculat el gradient sobre **totes** les flors a cada iteració. Amb milions de files
  això no es fa: s'agafa un grapat de files a l'atzar cada vegada (*descens de gradient
  estocàstic*), i el gradient surt més brut però molt més barat.

### I ara què

El mecanisme d'aquest quadern no és una cosa de la regressió logística. És **el** mecanisme.

Una xarxa neuronal és una funció amb molts més pesos, i s'entrena amb aquestes mateixes
cinc línies: calcular la pèrdua, calcular-ne el gradient, restar-lo multiplicat per $\eta$,
repetir. L'única peça que caldrà afegir és com es calcula el gradient quan la funció és una
composició de moltes capes, i la resposta és la regla de la cadena de la secció 6 aplicada
capa a capa, de l'última a la primera. Té nom, **retropropagació**, i és la mateixa
cancel·lació que hem vist al pas 3 repetida tantes vegades com capes hi hagi.

Quan arribeu al bloc de *deep learning* i vegeu `loss.backward()` i `optimizer.step()`,
això és el que hi ha a sota: el gradient que hem verificat a la secció 7 i la resta de la
secció 3.
"""))

info = escriu(cells, "Machine Learning/03_matematiques/MA_02_descens_gradient.ipynb",
              titol_colab="MA_02_descens_gradient.ipynb")
print(info)
